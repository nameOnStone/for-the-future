<template>
  <div class="common-layout">
    <el-container>
      <asider></asider>
      <el-container>
        <el-header height="100px">股票指标</el-header>
        <content></content>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import asider from "./asider.vue"
import content from "./content.vue"
export default {
  name: 'Index',
  components: {
    asider,
    content
  }
}
</script>

<style lang="scss">
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
  background-color: rgba(30, 40, 40, 0.724);
}
</style>