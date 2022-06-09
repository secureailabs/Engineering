const stageNumberToString = (stage:number, dcinfo?:[boolean, boolean, string]):string => {
    switch (stage) {
        case 1: {
            return 'Waiting for approval by data owner.';
        }
        case 2: {
            return 'Waiting for activation by research organization.';
        }
        case 3: {
            if (!dcinfo) {
                return 'Digital contract activated.'
            }

            var message = 'Digital contract activated, '
            const [canProvisionDigitalContract, canDeprovisionDigitalContract, HostForVirtualMachines] = dcinfo
            switch (canDeprovisionDigitalContract) {
                case false: {
                    message += canProvisionDigitalContract ? 'waiting to be provisionned.' : `waiting for an Azure template to be selected by the ${dcinfo[2]}.`
                    break;
                }
                case true: {
                    message += 'provisionned.'
                    break;
                }
            }
            return message
        }
        default: {
            return 'Information Unavailable'
        }
    }
}

export default stageNumberToString;