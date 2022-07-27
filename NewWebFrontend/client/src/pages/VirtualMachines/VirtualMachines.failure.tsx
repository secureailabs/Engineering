import React from 'react';

import { TVirtualMachinesFailureProps } from "./VirtualMachines.types";

const VirtualMachinesFailure: React.FC<TVirtualMachinesFailureProps> = () => {
  return (
    <p>There was an error fetching secure computation nodes. Please try again later</p>
  );
};

export default VirtualMachinesFailure;
