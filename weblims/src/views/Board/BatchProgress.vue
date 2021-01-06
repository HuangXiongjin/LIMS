<template>
    <el-row class="container mgt24">
        <el-col :span='24' class="mgt24 container mgb10">
            <div class="mgb24 fsz14px">当前批次流程</div>
            <el-steps :active="currentstep" finish-status="success">
                <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                    <template slot="description" v-if='item.User'>
                        <div><span>姓名：</span><span>{{item.User}}</span></div>
                        <div><span>时间：</span><span>{{item.OperationTime}}</span></div>
                    </template>
                </el-step>
            </el-steps>
        </el-col>
        <el-row>
            <el-col :span='3' class="mgr15 boxshadow">
               <el-select v-model="searchObj.category" placeholder="物料类">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span='3' class="mgr15 boxshadow">
               <el-select v-model="searchObj.status" placeholder="状态">
                    <el-option
                    v-for="item in opstate"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span='2' class="boxshadow req">
                <el-button type='primary' @click="SearchTab">查询</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-row class="container mgt24" style="height:400px;">
                <el-col :span='24' style="borderBottom:1px solid #ccc;" class="padd15">
                    <span class="fontWet titl" style="display:inline-block;height:40px;lineHeight:36px;">样本记录</span>
                </el-col>
                <el-col :span='24' class="mgt24">
                    <el-table
                        :data="batchTableData.data"
                        size='small'
                        highlight-current-row
                        style="width: 100%"
                        @row-click="handletabClick"
                        >
                        <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
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
        </el-row>
        </el-row>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           currentstep:5,
           batchinfo:[],
           showstep:false,
           searchObj:{
               category:'玉米淀粉',
               status:'质检'
           },
           batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            options: [{
                value: '选项1',
                label: '物料一'
                }],
            batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
            opstate: [{value: '申请',label: '申请'}, {value: '请验审核',label: '请验审核'},{value: '取样',label: '取样'},{value: '接收',label: '接收'},
            {value: '分发',label: '分发'},{value: '质检',label: '质检'},{value: '报告',label: '报告'},{value: '质检审核',label: '质检审核'},{value: '放行',label: '放行'}],
            batchtableconfig:[{prop:'Name',label:"样本品名"},{prop:'ProductNumber',label:'样本批次'},{prop:'VerifyDate',label:'登记时间',width:210},{prop:'VerifyUser',label:'登记人'},{prop:'ProductType',label:'类型'},{prop:'Status',label:'状态'}],//批次列表

        }
    },
    created(){
        this.getSelectOption()
        this.SearchTab()
    },
    methods: {
        handletabClick(row){ //点击行显示
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getCurrentSteps(CheckProjectNO){ //获取进度条
           var params={
                Action:'p',
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                   this.currentstep=res.data.data.length
                   this.batchinfo=this.batchinfo.map((item) => { //清空缓存的状态
                       return {Status:item.Status}
                   })
                   this.batchinfo.splice(0,res.data.data.length)
                   this.batchinfo=res.data.data.concat(this.batchinfo)
                }else{
                    this.$message({
                        type:'info',
                        message:'获取数据失败，请重试'
                    })
                }
            })
        },
        getSelectOption() { //获取下拉列表选项
           this.axios.get('/lims/AllProduct').then((res) => {
               if(res.data.code=='1000'){
                  this.options=res.data.data.map((item) => {
                      return {
                          value:item,
                          label:item
                      }
                  })
               }

           })
        },
        SearchTab(){ //查询相关数据
            var params={
                PerPage:this.batchTableData.limit,
                Page:this.batchTableData.offset,
                Status:this.searchObj.status,
                Product:this.searchObj.category
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.data.length==0){
                    this.showstep=false
                    }
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        },
    },
}
</script>
<style scoped>

</style>