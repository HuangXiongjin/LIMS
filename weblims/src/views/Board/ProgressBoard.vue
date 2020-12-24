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
                <el-steps :active="currentstep" finish-status="success">
                    <el-step title="请验审核" @click.native="selectStatus('请验审核',0)" class="cursor"></el-step>
                    <el-step title="取样" @click.native="selectStatus('取样',1)" class="cursor"></el-step>
                    <el-step title="接收" @click.native="selectStatus('接收',2)" class="cursor"></el-step>
                    <el-step title="分发" @click.native="selectStatus('分发',3)" class="cursor"></el-step>
                    <el-step title="质检" @click.native="selectStatus('质检',4)" class="cursor"></el-step>
                    <el-step title="报告" @click.native="selectStatus('报告',5)" class="cursor"></el-step>
                    <el-step title="质检审核" @click.native="selectStatus('质检审核',6)" class="cursor"></el-step>
                    <el-step title="放行" @click.native="selectStatus('放行',7)" class="cursor"></el-step>
                </el-steps>
            </el-col>
            <el-col :span='24' class="mgt24 container">
                <el-dialog title="当前批次进度" :visible.sync="dialogTableVisible" width='90%'>
                    <el-steps :active="currentstep" finish-status="success">
                        <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                            <template slot="description">
                                <div><span>姓名：</span><span>{{item.User}}</span></div>
                                <div><span>时间：</span><span>{{item.OperationTime}}</span></div>
                            </template>
                        </el-step>
                    </el-steps>
                    <div slot="footer" class="dialog-footer">
                        <el-button type="success" @click="dialogTableVisible = false">知道了</el-button>
                    </div>
                </el-dialog>
                <div class="padd15">当前进度下样本批次列表</div>
                <el-col>
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                   >
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handleLook(scope.row)" type="text" size="small" class="bledit">查看批次进度</el-button>
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
            dialogTableVisible:false,
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           batchtableconfig:[{prop:'Name',label:"样本品名"},{prop:'ProductNumber',label:'样本批次'},{prop:'VerifyDate',label:'登记时间',width:210},{prop:'VerifyUser',label:'登记人'},{prop:'ProductType',label:'类型'},{prop:'Status',label:'状态'}],//批次列表
           currentstep:1,
           currentstate:'审核',
           treeDom:[],
           defaultProps: {
            children: 'children',
            label: 'label'
            },
            currentgoods:'玉米淀粉',
            batchinfo:[]
        }
    },
    created(){
        this.getInitTree()
        this.selectStatus()
    },
    methods: {
        handleLook(row){//单条触发
            this.dialogTableVisible=true
            var params={
                Action:'p',
                CheckProjectNO:row.CheckProjectNO
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                    this.batchinfo=res.data.data
                }else{
                    this.$message({
                        type:'info',
                        message:'获取数据失败，请重试'
                    })
                }
            })
        },
        selectStatus(sta,index){ //点击步骤条
            if(sta==undefined){
                
            }else{
                this.currentstep=index
                this.currentstate=sta
            }
            var params={
                PerPage:this.batchTableData.limit,
                Page:this.batchTableData.offset,
                Status:this.currentstate,
                Product:this.currentgoods
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })

        },
        getInitTree() { //获取初始树形结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        },
        showTabInfo(obj,data,node){ //点击树触发的事件
            this.currentgoods=obj.label
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.selectStatus()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.selectStatus()
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