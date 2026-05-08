https://21st.dev/community/components/shailendrakumar19999/table/default
You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
table.tsx
import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Paper } from "@mui/material";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 70 },
  { field: "firstName", headerName: "First name", width: 130 },
  { field: "lastName", headerName: "Last name", width: 130 },
  { field: "age", headerName: "Age", type: "number", width: 90 },
  {
    field: "fullName",
    headerName: "Full name",
    description: "This column has a value getter and is not sortable.",
    sortable: false,
    width: 160,
    valueGetter: (_, row) => `${row.firstName || ""} ${row.lastName || ""}`,
  },
];

const initialRows = [
  { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
  { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
  { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
  { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
  { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
  { id: 6, lastName: "Melisandre", firstName: null, age: 150 },
  { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
  { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
  { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
];

const paginationModel = { page: 0, pageSize: 5 };

export function BasicTable() {
  const [rows] = React.useState(initialRows);

  return (
    <Paper
      className="
        bg-white dark:bg-gray-900
        text-gray-900 dark:text-gray-100
        rounded-xl shadow-md p-1
      "
      sx={{
        height: 420,
        width: "100%",
        position: "relative",
        // let DataGrid cells inherit the Tailwind colors
        "& .MuiDataGrid-root": {
          color: "inherit",
          backgroundColor: "transparent",
        },
        "& .MuiDataGrid-cell": {
          borderColor: "rgba(156,163,175,0.2)", // gray-400/20
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{
          border: 0,
          color: "inherit",
          backgroundColor: "transparent",
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: "transparent",
            color: "inherit",
          },
        }}
      />
    </Paper>
  );
}


demo.tsx
import React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BasicTable } from "@/components/ui/table";

export default function DemoOne() {
  const [dark, setDark] = React.useState(
    () => document.documentElement.classList.contains('dark') // initial read
  );

  React.useEffect(() => {
    // keep Tailwind dark class in sync
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode: dark ? 'dark' : 'light',
        },
      }),
    [dark]
  );
  return <ThemeProvider theme={theme} className="w-full">
      <BasicTable />
    </ThemeProvider>
}

```

Install NPM dependencies:
```bash
@mui/material, @mui/x-data-grid
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them
import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Paper } from "@mui/material";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 70 },
  { field: "firstName", headerName: "First name", width: 130 },
  { field: "lastName", headerName: "Last name", width: 130 },
  { field: "age", headerName: "Age", type: "number", width: 90 },
  {
    field: "fullName",
    headerName: "Full name",
    description: "This column has a value getter and is not sortable.",
    sortable: false,
    width: 160,
    valueGetter: (_, row) => `${row.firstName || ""} ${row.lastName || ""}`,
  },
];

const initialRows = [
  { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
  { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
  { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
  { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
  { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
  { id: 6, lastName: "Melisandre", firstName: null, age: 150 },
  { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
  { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
  { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
];

const paginationModel = { page: 0, pageSize: 5 };

export function BasicTable() {
  const [rows] = React.useState(initialRows);

  return (
    <Paper
      className="
        bg-white dark:bg-gray-900
        text-gray-900 dark:text-gray-100
        rounded-xl shadow-md p-1
      "
      sx={{
        height: 420,
        width: "100%",
        position: "relative",
        // let DataGrid cells inherit the Tailwind colors
        "& .MuiDataGrid-root": {
          color: "inherit",
          backgroundColor: "transparent",
        },
        "& .MuiDataGrid-cell": {
          borderColor: "rgba(156,163,175,0.2)", // gray-400/20
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{
          border: 0,
          color: "inherit",
          backgroundColor: "transparent",
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: "transparent",
            color: "inherit",
          },
        }}
      />
    </Paper>
  );
}

---

## Contact360 adoption (production)

This file is a **third-party integration recipe** (MUI X DataGrid + MUI Paper + Tailwind class names on the shell). The Contact360 app does **not** ship this stack for list pages.

**What we use instead**

- **`c360-*` design tokens** and semantic HTML `<table>` for dense product grids, or shared primitives under `contact360.io/app/src/components/ui/` (`DataTable`, `Table`, [`C360DataTableShell`](../../../../contact360.io/app/src/components/ui/C360DataTableShell.tsx) for card-like shells + scroll regions).
- A factual inventory of `<table>` usage in the app lives in [`docs/frontend/data-tables-inventory.md`](../data-tables-inventory.md).
- Page-level flow and stack decision (no MUI for lists): [`docs/frontend/hiring-signals-page-anatomy.md`](../../hiring-signals-page-anatomy.md).

**Reference implementation**

- **Hiring signals** (`HiringSignalsDataTable`, hiring-signals dashboard route): **server-driven** column sort, row selection, optional column visibility, and toolbar page size — same *product* goals as the snippet above (checkboxes, paging, sortable columns) without MUI.

When adding a new data grid, prefer extending existing `c360` patterns rather than pasting this MUI snippet unless there is an explicit decision to add `@mui/material` and `@mui/x-data-grid` to the app.
