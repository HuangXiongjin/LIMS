<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24">
            <el-row class="container">
                <el-col :span='4' class="mgr15">
                    <el-input
                        placeholder="类别/品名"
                        prefix-icon="el-icon-search"
                        v-model="searchObj.category">
                    </el-input>
                </el-col>
                <el-col :span='4' class="mgr15">
                    <el-select v-model="searchObj.goods" placeholder="物料类">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </el-col>
                <el-col :span='4' class="mgr15">
                      <el-date-picker
                        v-model="searchObj.registrydate"
                        type="date"
                        placeholder="选择日期">
                      </el-date-picker>
                </el-col>
            </el-row>
        </el-col>
        <el-col :span='24' class="mgt24">
            <div class="container">
                <el-menu :default-active="'1'" class="bgwhite" mode="horizontal" @select="handleSelect">
                    <el-menu-item :index="'1'">处理中心</el-menu-item>
                    <el-menu-item :index="'2'">处理中心</el-menu-item>
                </el-menu>
                <div class="mgt24" v-if="currentChoose==='1'">
                    23344
                </div>
                <div class="mgt24" v-if="currentChoose==='2'">456</div>
            </div>
        </el-col>
    </el-row>
</template>
<script>
export default {
    data(){

        return {
           msg:'12',
           searchObj:{
               category:'',
               registrydate:'',
               goods:'',
           },
            options: [{
                value: '选项1',
                label: '物料一'
                }, {
                value: '选项2',
                label: '物料二'
                }],
            currentChoose:'1', 
        }
    },
    methods: {
        handleSelect(key) {
            this.currentChoose=key
        }
    },
}
</script>
<style scoped>

</style>