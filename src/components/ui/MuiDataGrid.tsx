"use client";

import {
  DataGrid,
  type GridColDef,
  type GridRowParams,
  type GridRowSelectionModel,
} from "@mui/x-data-grid";
import { C360MuiThemeProvider } from "@/components/ui/C360MuiThemeProvider";
import { C360DataTableShell } from "@/components/ui/C360DataTableShell";

export interface MuiDataGridProps {
  rows: Record<string, unknown>[];
  columns: GridColDef[];
  loading?: boolean;
  autoHeight?: boolean;
  checkboxSelection?: boolean;
  rowSelectionModel?: GridRowSelectionModel;
  onRowSelectionModelChange?: (model: GridRowSelectionModel) => void;
  onRowClick?: (params: GridRowParams) => void;
}

/** MUI DataGrid wrapped with c360 theme + table shell (admin list pages). */
export function MuiDataGrid({
  rows,
  columns,
  loading = false,
  autoHeight = false,
  checkboxSelection = false,
  rowSelectionModel,
  onRowSelectionModelChange,
  onRowClick,
}: MuiDataGridProps) {
  return (
    <C360MuiThemeProvider>
      <C360DataTableShell>
        <DataGrid
          rows={rows}
          columns={columns}
          loading={loading}
          autoHeight={autoHeight}
          checkboxSelection={checkboxSelection}
          rowSelectionModel={rowSelectionModel}
          onRowSelectionModelChange={onRowSelectionModelChange}
          onRowClick={onRowClick}
          disableRowSelectionOnClick={!checkboxSelection}
          pageSizeOptions={[10, 25, 50]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          sx={{ border: 0, minHeight: autoHeight ? undefined : 400 }}
        />
      </C360DataTableShell>
    </C360MuiThemeProvider>
  );
}
