const accountStatusNumberToString = (number: 0 | 1 | 2 | 3) => {
  switch (number) {
    case 0: return 'New';
    case 1: return 'Open';
    case 2: return 'Suspended';
    case 3: return 'Closed';
  }
};

export default accountStatusNumberToString;
