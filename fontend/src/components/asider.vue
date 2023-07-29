<template>
    <el-aside width="200px">
        <el-scrollbar height="500px">
            <!-- <el-menu :default-openeds="['1', '3']"> -->
            <el-menu>
                <el-sub-menu index="1">
                    <template #title>
                        <el-icon>
                            <message />
                        </el-icon>百日新增
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="1-1">Option 1</el-menu-item>
                        <el-menu-item index="1-2">Option 2</el-menu-item>
                    </el-menu-item-group>
                </el-sub-menu>
            </el-menu>
        </el-scrollbar>
    </el-aside>
</template>

<script>
export default {
    name: 'asider',
}

</script>