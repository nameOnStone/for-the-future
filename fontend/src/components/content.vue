<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="grid-content ep-bg-purple" style="color:#fff">
          <IndustryLineChart></IndustryLineChart>
        
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24"> 
        <div class="grid-content ep-bg-purple">
          <stock-table></stock-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import StockTable from "./stockTable.vue"
import IndustryLineChart from "./IndustryLineChart.vue";


export default {
  name: "content",
  components:{
    StockTable,
    IndustryLineChart,
  }
}

</script>