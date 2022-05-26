// export type TPutVirtualMachineStart = {};

// export type TPutVirtualMachineSuccess = null;

// export type TGetVirtualMachineSuccess = {
//     VirtualMachineGuid: string;
//     DigitalContractGuid: string;
//     DigitalContractTitle: string;
//     RegistrationTime: number;
//     HeartbeatBroadcastTime: number;
//     IPAddress: string;
//     NumberOfVCPU: number;
//     HostRegion: string;
//     StartTime: number;
//     State?: string;
//     VMLoggedInUser?: string;
//     Note: string;
// };

// export type TGetVirtualMachineStart = {
//     VirtualMachineGuid: string;
// };

// export type TGetAllVirtualMachinesSuccess = Record<
//     string,
//     {
//         HostForVirtualMachines: 'Researcher' | 'Data Owner';
//         ResearcherOrganization: string;
//         DataOwnerOrganization: string;
//         VirtualMachinesAssociatedWithDc: Record<string, TGetVirtualMachineSuccess>;
//     }
// >;

// export type TGetAllVirtualMachinesStart = null;

export {}