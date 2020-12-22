<template>
    <el-row :gutter='20'>
        <el-col :span='24'>
            <el-row class="container mgt24">
                <el-col :span='24'>
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
                           <el-select v-model="searchObj.status" placeholder="物料类">
                                <el-option
                                v-for="item in Status"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span='3' class="mgr15 boxshadow">
                           <el-date-picker
                            v-model="searchObj.registrydate"
                            type="date"
                            placeholder="选择日期">
                           </el-date-picker>
                        </el-col>
                        <el-col :span='2' class="boxshadow req">
                            <el-button type='primary' @click="SearchTab">查询</el-button>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
        </el-col>
        <el-col :span='24'>
            <div class="container mgt24" style="height:400px;">
                <el-col :span='24' style="borderBottom:1px solid #ccc;" class="padd15">
                    <span class="fontWet titl" style="display:inline-block;height:40px;lineHeight:36px;">留样清单</span>
                </el-col>
                <el-col :span='24' class="mgt24">
                    <el-table
                        :data="batchTableData.data"
                        size='small'
                        highlight-current-row
                        style="width: 100%"
                        @row-click="handletabClick">
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
            </div>
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
           Row:{},
           distribute:{
               CheckProjectNO:'',
           },
           searchObj:{
               category:'玉米淀粉',
               registrydate:moment(new Date()).format('YYYY-MM-DD'),
               status:'留样观察中'
           },
           options: [{
                value: '选项1',
                label: '物料一'
                }],
           Status: [{value: '1',label: '待接收'},{value: '2',label: '留样观察中'},{value: '3',label: '申请销毁'}],
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            xfopt:true,
            batchtableconfig:[
                {prop:'Name',label:'品名'},{prop:'Specs',label:'规格'},{prop:'PackSpecs',label:'包装规格'},
                {prop:'ProductNumber',label:'产品批号'},{prop:'TheoreticalYield',label:'理论产量'},{prop:'BatchAmount',label:'留样数量'},
                {prop:'BatchDepartment',label:'留样部门'},{prop:'BatchName',label:'留样人'},{prop:'Position',label:'留样位置'},
                {prop:'BatchTime',label:'留样时间'},{prop:'Handler',label:'留样人'},{prop:'ProductionDate',label:'生产日期'},
                {prop:'ValidityDate',label:'有效日期'},{prop:'Comment',label:'备注'}
            ],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
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
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD"),
                Status:this.searchObj.status
            }
            this.axios.get('/lims/ProductSaveList',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.xfopt=false
            this.Row=row
            this.distribute.CheckProjectNO=row.CheckProjectNO
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