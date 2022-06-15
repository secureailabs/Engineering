import {
  TGetAllDatasetsStart,
  TGetAllDatasetsSuccess,
  TGetDatasetSuccess,
  TGetDatasetStart,
} from './dataset.typeDefs';
import demo_data from './dataset.data';

export const getDatasetAPIdemo = async (data: TGetDatasetStart): Promise<TGetDatasetSuccess> => {
  const index = parseInt(data.dataset_id.slice(-1)) - 1

  // @ts-ignore
  return demo_data.datasets[index];
}

export const getAllDatasetsAPIdemo = async ({ data }: { data: TGetAllDatasetsStart }): Promise<TGetAllDatasetsSuccess['datasets']> => {
  // @ts-ignore
  return demo_data.datasets;
}
