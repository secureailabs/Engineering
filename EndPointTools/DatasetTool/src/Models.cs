class ModelDataset
{
    public string name { get; set; } = default!;
    public string description { get; set; } = default!;
    public string tags { get; set; } = default!;
    public string state { get; set; } = default!;
    public string format { get; set; } = default!;
}


class ModelDatasetVersionMetadata
{
    public Guid dataset_id { get; set; } = default!;
    public string description { get; set; } = default!;
    public string name { get; set; } = default!;
    public string tags { get; set; } = default!;
    public string state { get; set; } = default!;
}

class DatasetHeader
{
    public ModelDatasetVersionMetadata dataset_version { get; set; } = default!;
    public string aes_tag { get; set; } = default!;
    public string aes_nonce { get; set; } = default!;
}
