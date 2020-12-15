<template>
    <el-row :gutter="20" class="mgt24">
        <el-col :span='5'>
            <el-col class="container">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                    <el-tree
                    :data="treeDom"
                    node-key="id"
                    default-expand-all
                    :expand-on-click-node="false"
                    :props="defaultProps"
                    highlight-current
                    @node-click='showTabInfo'>
                    </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='19'>
            <el-col :span='24' class="container">
                <el-steps :active="currentstep" status='finish'>
                    <el-step title="步骤 1" name='description'>
                        <template slot="description" >
                            <div><span>人物：</span><span>张三</span></div>
                            <div><span>时间：</span><span>2020-12-14 14:09:12</span></div>
                        </template>
                    </el-step>
                    <el-step title="步骤 2" name='description'>
                        <template slot="description" >
                            <div><span>人物：</span><span>李四</span></div>
                            <div><span>时间：</span><span>2020-12-14 14:09:12</span></div>
                        </template>
                    </el-step>
                    <el-step title="步骤 3" name='description'>
                        <template slot="description" >
                            <div><span>人物：</span><span></span></div>
                            <div><span>时间：</span><span></span></div>
                        </template>
                    </el-step>
                </el-steps>
            </el-col>
            <el-col :span='24' class="mgt24 container">
                <div>当前进度下样本批次列表</div>
                <el-col>
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handlePass(scope.row)" type="text" size="small" class="bledit">通过</el-button>
                            <el-button @click.native.prevent="handleBack(scope.row)" type="text" size="small" class="redde">驳回</el-button>
                        </template>
                    </el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                    </div>
                </el-col>
            </el-col>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){

        return {
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           batchtableconfig:[{prop:'Specs',label:"规格"},{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'Supplier',label:'供货单位'},{prop:'Number',label:'物料编码'},{prop:'Amount',label:'数量'},{prop:'Unit',label:'单位'},{prop:'CheckDate',label:'请验时间'}],//批次列表
           currentstep:1,
           treeDom:[],
           defaultProps: {
            children: 'children',
            label: 'label'
            },
            currentgoods:'物料类'
        }
    },
    created(){
        this.getInitTree()
        this.getInitTab()
    },
    methods: {
        getInitTree() { //获取初始树形结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        },
        showTabInfo(obj,data,node){ //点击数触发的事件
            console.log(obj)
            console.log(data)
            console.log(node)
        },
        getInitTab(){
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:this.searchObj.registrydate,
                Status:this.searchObj.state
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.getInitTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.getInitTab()
        }
    },
}
</script>
<style scoped>
    .titl{
        height:46px;
        line-height:46px;
        border-bottom:1px solid #ccc;
    }
    .jbform .el-select{
        width: 100%;
    }
</style>