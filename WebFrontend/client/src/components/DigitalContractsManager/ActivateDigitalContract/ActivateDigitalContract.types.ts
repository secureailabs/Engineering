import { IDefaults } from '@redux/typedefs';
import {
  TGetDigitalContractSuccess,
  TPatchActivateDigitalContractStart,
} from '@redux/digitalContract/digitalContract.typeDefs';

export type TActivateDigitalContractProps = {
  patchActivateDigitalContractStart(
    data: TPatchActivateDigitalContractStart
  ): void;
  patchActivateDigitalContractReset(): void;
  patchActivateDigitalContractState: IDefaults['state'];
  getDigitalContractData: TGetDigitalContractSuccess | null;

  DigitalContractGuid: string;
};

export type TActivateDigitalContactFormProps = {
  patchActivateDigitalContractStart(
    data: TPatchActivateDigitalContractStart
  ): void;
  patchActivateDigitalContractReset(): void;
  getDigitalContractData: TGetDigitalContractSuccess | null;

  DigitalContractGuid: string;
};
