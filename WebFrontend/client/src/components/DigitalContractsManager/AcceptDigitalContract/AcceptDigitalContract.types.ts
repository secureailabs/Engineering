import { IDefaults } from '@redux/typedefs';
import { TPatchAcceptDigitalContractStart } from '@redux/digitalContract/digitalContract.typeDefs';

export type TAcceptDigitalContractProps = {
  patchAcceptDigitalContractStart(data: TPatchAcceptDigitalContractStart): void;
  patchAcceptDigitalContractReset(): void;
  patchAcceptDigitalContractState: IDefaults['state'];
  DigitalContractGuid: string;
};

export type TAcceptDigitalContactFormProps = {
  patchAcceptDigitalContractStart(data: TPatchAcceptDigitalContractStart): void;
  patchAcceptDigitalContractReset(): void;
  DigitalContractGuid: string;
};
