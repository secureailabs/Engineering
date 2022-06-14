import { TGetAllVirtualMachinesSuccess } from "./virtualMachineManager.typedefs";

const demo_data : TGetAllVirtualMachinesSuccess = {
    secure_computation_nodes: [
        {
            id: 'uuid1',
            name: 'MGR Main Node',
            digital_contract: {
                id: 'uuid1',
                name: 'IGR-MGR contract'
            },
            dataset: {
                id: 'uuid1',
                name: 'IGR Dataset #12'
            },
            researcher: {
                id: 'uuid2',
                name: 'Mercy General Hospital'
            },
            data_owner: {
                id: 'uuid1',
                name: 'International Genetics Research Facility'
            },
            researcher_user: {
                id: 'uuid1',
                name: 'Nick Adams'
            },
            type: 'Standard_D4s_v4',
            timestamp: '2075-05-30T20:17:32.522Z',
            state: 'READY',
            detail: 'Nick Adams is the only person allowed to use this SCN.',
            ipaddress: '198.51.100.42'
        }
    ]
}

export default demo_data