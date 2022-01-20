export type TInfoDisplay = {
  title?: string;
  data: Array<{
    section_title: string;
    section_data: any;
    data_parser?: (data: any) => any;
    conditional?: boolean;
    to_locale_date_string?: boolean;
    color?: string;
  }>;
};
