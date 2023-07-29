<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="grid-content ep-bg-purple" style="color:#fff">图</div>
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

export default {
  name: "content",
  components:{
    StockTable,
  }
}

</script>