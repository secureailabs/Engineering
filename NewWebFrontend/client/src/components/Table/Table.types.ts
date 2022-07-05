import type { TableState, Column } from 'react-table';

type TTable = {
  columns: readonly Column<object>[];
  data: readonly object[];
  initial_state?: TableState<object>;
  id_accessor?: string;
  base_url?: string;
  show_head?: boolean;
};

export default TTable;
