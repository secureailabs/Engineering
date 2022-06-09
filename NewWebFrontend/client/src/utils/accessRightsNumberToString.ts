const accessRightsNumberToString = (number: 1 | 2 | 3 | 4 | 5 | 6 ) => {
  switch (number) {
    case 1: return 'Admin';
    case 2: return 'Auditor';
    case 3: return 'User';
    case 4: return 'Digital Contract Admin';
    case 5: return 'Dataset Admin';
    case 6: return 'SAIL Admin';
  }
};

export default accessRightsNumberToString;
