import {
    TGetUnifiedRegistryStart,
    TGetAllUnifiedRegistriesStart,
    TGetUnifiedRegistrySuccess,
    TGetAllUnifiedRegistriesSuccess,
} from './unifiedRegistry.types';

import { demo_data } from './unifiedRegistry.data';

export const getUnifiedRegistryAPIdemo = async (data: TGetUnifiedRegistryStart): Promise<TGetUnifiedRegistrySuccess> => {
    // @ts-ignore
    return demo_data.UnifiedRegistries[data.ID || ""];
}

export const getAllUnifiedRegistriesAPIdemo = async (data: TGetAllUnifiedRegistriesStart): Promise<TGetAllUnifiedRegistriesSuccess> => {
    // @ts-ignore
    return demo_data
}
