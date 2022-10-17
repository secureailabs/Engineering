class Dataset
{
    public string name { get; set; } = default!;
    public string description { get; set; } = default!;
    public string tags { get; set; } = default!;
    public string state { get; set; } = default!;
}


class DatasetVersionMetadata
{
    public Guid dataset_id { get; set; } = default!;
    public string description { get; set; } = default!;
    public string name { get; set; } = default!;
    public string tags { get; set; } = default!;
    public string state { get; set; } = default!;
}

