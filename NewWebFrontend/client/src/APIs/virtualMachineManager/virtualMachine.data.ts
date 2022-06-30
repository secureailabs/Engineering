import { TGetAllVirtualMachinesSuccess } from "./virtualMachineManager.typedefs";

// const demo_data : TGetAllVirtualMachinesSuccess = {
//     secure_computation_nodes: [
//         {
//             id: 'uuid1',
//             name: 'MGR Main Node',
//             digital_contract: {
//                 id: 'uuid1',
//                 name: 'IGR-MGR contract'
//             },
//             dataset: {
//                 id: 'uuid1',
//                 name: 'IGR Dataset #12'
//             },
//             researcher: {
//                 id: 'uuid2',
//                 name: 'Mercy General Hospital'
//             },
//             data_owner: {
//                 id: 'uuid1',
//                 name: 'International Genetics Research Facility'
//             },
//             researcher_user: {
//                 id: 'uuid1',
//                 name: 'Nick Adams'
//             },
//             type: 'Standard_D4s_v4',
//             timestamp: '2075-05-30T20:17:32.522Z',
//             state: 'READY',
//             detail: 'Nick Adams is the only person allowed to use this SCN.',
//             ipaddress: '198.51.100.42'
//         }
//     ]
// }

const demo_data: TGetAllVirtualMachinesSuccess = {
    secure_computation_nodes: [
        {
            id: 'uuid1',
            name: 'Sallie Demo VM',
            ipaddress: '198.51.100.42',
            type: 'Standard_D4s_v4',
            state: 'READY',

            // Fields not implemented in current backend but shown in demos
            region: 'East US 2',
            lauched_by: {
                user_name: 'Sallie Director',
                user_email: 'sallie@kidneycancer.org',
                org_name: 'Kidney Cancer Association',
                org_id: 'uuid1'
            },
            uptime: '≈ 1 hour',

            // Value used but now shown in current demo
            data_owner: {
                id: 'uuid1',
                name: 'International Genetics Research Facility'
            },

            // Values not shown in current demo
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
            researcher_user: {
                id: 'uuid1',
                name: 'Nick Adams'
            },
            timestamp: '2075-05-30T20:17:32.522Z',
            detail: 'Nick Adams is the only person allowed to use this SCN.',
        },
        {
            id: 'uuid2',
            name: 'Isabel Archer (KCA) VM',
            ipaddress: '193.21.140.45',
            type: 'Standard_D4s_v4',
            state: 'READY',

            // Fields not implemented in current backend but shown in demos
            region: 'East US 2',
            lauched_by: {
                user_name: 'Isabel Archer',
                user_email: 'iarcher@kidneycancer.org',
                org_name: 'Kidney Cancer Association',
                org_id: 'uuid1'
            },
            uptime: '≈ 3 hours',

            // Value used but now shown in current demo
            data_owner: {
                id: 'uuid1',
                name: 'International Genetics Research Facility'
            },

            // Values not shown in current demo
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
            researcher_user: {
                id: 'uuid1',
                name: 'Nick Adams'
            },
            timestamp: '2075-05-30T20:17:32.522Z',
            detail: 'Nick Adams is the only person allowed to use this SCN.',
        },
        {
            id: 'uuid3',
            name: 'PCR Demo VM',
            ipaddress: '192.53.100.10',
            type: 'Standard_D4s_v4',
            state: 'READY',

            // Fields not implemented in current backend but shown in demos
            region: 'East US 2',
            lauched_by: {
                user_name: 'Robert Johnson',
                user_email: 'robert@crh.org',
                org_name: 'Cancer Research Hospital',
                org_id: 'uuid2'
            },
            uptime: '≈ 2 hours',

            // Value used but now shown in current demo
            data_owner: {
                id: 'uuid1',
                name: 'Kidney Cancer Association'
            },

            // Values not shown in current demo
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
            researcher_user: {
                id: 'uuid1',
                name: 'Nick Adams'
            },
            timestamp: '2075-05-30T20:17:32.522Z',
            detail: 'Nick Adams is the only person allowed to use this SCN.',
        }
    ]
}

export default demo_data