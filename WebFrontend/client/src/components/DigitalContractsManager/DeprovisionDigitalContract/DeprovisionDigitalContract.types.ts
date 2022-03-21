import { IDefaults } from '@redux/typedefs';
import {
  TGetDigitalContractSuccess,
  TDeprovisionDigitalContractStart,
} from '@redux/digitalContract/digitalContract.typeDefs';

export type TDeprovisionDigitalContractProps = {
  deprovisionDigitalContractStart(
    data: TDeprovisionDigitalContractStart
  ): void;
  deprovisionDigitalContractReset(): void;
  deprovisionDigitalContractState: IDefaults['state'];
  DigitalContractGuid: string;
};

export type TDeprovisionDigitalContactFormProps = {
  deprovisionDigitalContractStart(
    data: TDeprovisionDigitalContractStart
  ): void;

  DigitalContractGuid: string;
};
