export type TGetAllDatasetsStart = {
  data_owner_id?: string;
}

export type TGetAllDatasetsSuccess = {
  datasets: Array<TGetDatasetSuccess>;
};


export type TGetDatasetSuccess = {
  id: string;
  description: string;
  name: string;
  keywords: string;
  version: string;
  publish_date: number;
  tables: Array<{
    id: string;
    number_of_rows: number;
    name: string;
    tags: string;
    number_of_columns: number;
    compressed_data_size_in_bytes: number;
    description: string;
    all_column_properties: Array<{
      id: string;
      units: string;
      name: string;
      tags: string;
      type: string;
      description: string;
    }>
  }>
};

export type TGetDatasetStart = {
  dataset_id: string;
};