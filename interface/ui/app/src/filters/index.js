const snippet = (s) => {
  const snipped = s.slice(0, 100);
  return `${snipped}...`;
};

const uppercase = s => s.toUpperCase();


export default {
  snippet,
  uppercase,
};
