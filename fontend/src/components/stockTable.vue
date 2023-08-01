<template>
  <!-- <button @click="deselectRows">deselect rows</button> -->
    <!-- :defaultColDef="defaultColDef" -->
  <ag-grid-vue
    class="ag-theme-alpine"
    style="height: 400px"
    :columnDefs="columnDefs.value"
    :rowData="rowData.value"
    rowSelection="multiple"
    animateRows="true"
    @cell-clicked="cellWasClicked"
    @grid-ready="onGridReady"
  >
  </ag-grid-vue>
</template>

<script>
import { AgGridVue } from "ag-grid-vue3";  // the AG Grid Vue Component
import { reactive, onMounted, ref } from "vue";


export default {
  name: "StockTable",
  components: {
    AgGridVue,
  },
  setup() {
    const gridApi = ref(null); // Optional - for accessing Grid's API

    // Obtain API from grid's onGridReady event
    const onGridReady = (params) => {
      gridApi.value = params.api;
      // gridApi.value.sizeColumnsToFit()
    };

    const rowData = reactive({}); // Set rowData to Array of Objects, one Object per Row

    // Each Column Definition results in one Column.
    const columnDefs = reactive({
      value: [
            { field: "序号" , width:100, 'pinned': 'left'},
            { field: "代码" , width:100, 'pinned': 'left'},
            { field: "名称" , width:120, 'pinned': 'left'},
            { field: "最新价" , width:100},
            { field: "涨跌幅" , width:100},
            { field: "涨跌额" , width:100},
            { field: "成交量" , width:100},
            { field: "成交额" , width:150},
            { field: "振幅" , width:100},
            { field: "最高" , width:100},
            { field: "最低" , width:100},
            { field: "今开" , width:100},
            { field: "昨收" , width:100},
            { field: "量比" , width:100},
            { field: "换手率" , width:100},
            { field: "市盈率-动态" , width:150},
            { field: "市净率" , filter: "agNumberColumnFilter"},
            { field: "总市值" },
            { field: "流通市值" },
            { field: "涨速" },
            { field: "5分钟涨跌" },
            { field: "60日涨跌幅" },
            { field: "年初至今涨跌幅" },
            { field: "是否百日新高", filter: "agTextColumnFilter"},
            { field: "百日新高价格" },
            { field: "所属行业", filter: "agTextColumnFilter"},
            { field: "距百日新高有多少个交易日" },
            { field: "百日标准差", filter: "agNumberColumnFilter"},
            { field: "连涨天数" },
            { field: "昨日新高与今日新高", filter: "agTextColumnFilter" },
            { field: "所属行业新高股票数"},
      ],
    });

    // DefaultColDef sets props common to all Columns
    const defaultColDef = {
      sortable: true,
      filter: true,
      flex: 1
    };

    // Example load data from server
    onMounted(() => {
      fetch("http://localhost:9999/db/test")
        .then((result) => result.json())
        .then((remoteRowData) => (rowData.value = remoteRowData));
    });

    return {
      onGridReady,
      columnDefs,
      rowData,
      defaultColDef,
      cellWasClicked: (event) => { // Example of consuming Grid Event
        console.log("cell was clicked", event);
      },
      deselectRows: () =>{
        gridApi.value.deselectAll()
      }
    };
  },
  data(){
    return {

    }
  }
};
</script>

<style lang="scss">
.ag-theme-alpine {
  /* disable all borders */
  // --ag-borders: 'red';
  --ag-font-size: "1px"
  /* then add back a border between rows */
  // --ag-row-border-style: dashed;
  // --ag-row-border-width: 5px;
  // --ag-row-border-color: rgb(150, 150, 200);
}
.ag-cell {
  border: 1px solid #1a1818
}

</style>
