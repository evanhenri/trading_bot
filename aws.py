#!/usr/bin/env python3
import argparse
import functools
import logging
import sys
import types
import uuid

import boto3
# credentials auto loaded from ~/.aws/credentials


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
log.addHandler(sh)

tld = 'nonce.ch'
k8s_domain = f'k8s.{tld}'
s3_bucket = f'state-store.{k8s_domain}'


class LogResp:
    """
    Exec order:
        __get__
        func
        __call__
    """
    def __init__(self, func):
        functools.wraps(func)(self)

    def __call__(self, *args, **kwargs):
        retval = self.__wrapped__(*args, **kwargs)
        log.info(f'{self.__wrapped__.__name__}: {retval}')
        return retval

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


class AWS:
    def __init__(self):
        name = self.__class__.__name__.lower()
        self._client = boto3.client(name)


class Route53(AWS):
    def __init__(self):
        super().__init__()

    def __contains__(self, hz_name):
        _hz_name = hz_name.rstrip('.') + '.'

        for hz_config in self.hosted_zones:
            if hz_config['Name'] == _hz_name:
                return True
        return False

    @LogResp
    def change_resource_record_sets(self, hz_name, change_batch, **kwargs):
        return self._client.change_resource_record_sets(
            HostedZoneId=self.get_hosted_zone_id(hz_name),
            ChangeBatch=change_batch,
            **kwargs
        )

    @LogResp
    def create_hosted_zone(self, hz_name, caller_reference=None, **kwargs):
        if caller_reference is None:
            caller_reference = str(uuid.uuid1())

        return self._client.create_hosted_zone(
            Name=hz_name,
            CallerReference=caller_reference,
            **kwargs
        )

    @LogResp
    def get_hosted_zone(self, hz_name):
        _hz_name = hz_name.rstrip('.') + '.'

        for hz in self.hosted_zones:
            if hz['Name'] == _hz_name:
                return hz

    @LogResp
    def get_hosted_zone_id(self, hz_name):
        return self.get_hosted_zone(hz_name=hz_name)['Id']

    @LogResp
    def get_resource_records(self, hz_name, record_type):
        records = []
        for rs in self.list_resource_record_sets(
                hz_id=self.get_hosted_zone_id(hz_name)
        ):
            if rs['Type'] == record_type:
                records.append(rs)
        return records

    @LogResp
    def list_resource_record_sets(self, hz_id, **kwargs):
        return self._client.list_resource_record_sets(
            HostedZoneId=hz_id,
            **kwargs
        )['ResourceRecordSets']

    @property
    @LogResp
    def hosted_zones(self):
        return self._client.list_hosted_zones()['HostedZones']


class S3(AWS):
    def __init__(self):
        super().__init__()

    def __contains__(self, bucket_name):
        for config in self.buckets:
            if config['Name'] == bucket_name:
                return True
        return False

    @property
    @LogResp
    def buckets(self):
        return self._client.list_buckets()['Buckets']

    @LogResp
    def create_bucket(self, name, region=None):
        return self._client.create_bucket(
            Bucket=name,
            **{
                'CreateBucketConfiguration': {
                    'LocationConstraint': region
                }
            } if region is not None else {}
        )

    @LogResp
    def put_bucket_versioning(self, name, enabled=True):
        return self._client.put_bucket_versioning(
            Bucket=name,
            VersioningConfiguration={
                'Status': 'Enabled'if enabled else 'Suspended'
            }
        )


def setup_aws():
    route53 = Route53()
    s3 = S3()

    if k8s_domain not in route53:
        route53.create_hosted_zone(k8s_domain)

    for ns_rr in route53.get_resource_records(tld, record_type='NS'):
        if ns_rr['Name'].startswith(k8s_domain):
            break
    else:
        k8s_ns_rrs = route53.get_resource_records(k8s_domain, record_type='NS')
        route53.change_resource_record_sets(
            tld,
            change_batch={
                'Comment': f'Create a subdomain NS record in the {tld} domain',
                'Changes': [{
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': k8s_domain,
                        'Type': 'NS',
                        'TTL': 300,
                        'ResourceRecords': k8s_ns_rrs[0]['ResourceRecords']
                    }
                }]
            }
        )

    if s3_bucket not in s3:
        s3.create_bucket(s3_bucket)


def route53_cname(cname):
    route53 = Route53()
    route53.change_resource_record_sets(
        k8s_domain,
        change_batch={
            'Comment': 'Update CNAME record to point to cluster ingress controller',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': f'ui.{k8s_domain}',
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [
                        {'Value': cname}
                    ]
                }
            }]
        }
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup-aws', action='store_true')
    parser.add_argument('--route53-cname', nargs=1)
    return parser.parse_args()

def main():
    args = parse_args()
    if args.setup_aws:
        setup_aws()
    if args.route53_cname:
        cluster_ingress_controller_cname = args.route53_cname[0]
        route53_cname(cluster_ingress_controller_cname)


if __name__ == '__main__':
    main()
