import { IDefaults } from '@redux/typedefs';
import {
  TGetDigitalContractSuccess,
  TProvisionDigitalContractStart,
} from '@redux/digitalContract/digitalContract.typeDefs';

export type TProvisionDigitalContractProps = {
  provisionDigitalContractStart(
    data: TProvisionDigitalContractStart
  ): void;
  provisionDigitalContractReset(): void;
  provisionDigitalContractState: IDefaults['state'];
  DigitalContractGuid: string;
};

export type TProvisionDigitalContactFormProps = {
  provisionDigitalContractStart(
    data: TProvisionDigitalContractStart
  ): void;

  DigitalContractGuid: string;
};
