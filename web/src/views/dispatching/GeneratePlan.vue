<template>
    <el-row>
        <el-col :span='24' class="productionstep">
            <el-steps :active="active" finish-status="success">
                <el-step title="步骤 1" icon="el-icon-edit"></el-step>
                <el-step title="步骤 2" icon="el-icon-upload"></el-step>
                <el-step title="步骤 3" icon="el-icon-picture"></el-step>
            </el-steps>
            <el-button style="margin-top: 12px;" @click="nextStep">下一步</el-button>
    </el-col>
    <el-col :span='24'>计划实际信息</el-col>
    <el-col :span='24'>计划实际信息</el-col>
    </el-row>
</template>
<script>
export default {
    data() {
        return {
            active:0,
        }
    },
    methods: {
        nextStep(){
            this.active++
            if(this.active==3){
                this.active=0
            }
        }
    },
}
</script>
<style scoped>
  .productionstep .el-steps--simple{
      background-color:#ddd;
  }
</style>