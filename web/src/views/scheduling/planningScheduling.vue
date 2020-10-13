<template>
  <el-row :gutter='20'>
    <el-col :span='9'>
      <div>
        <div class="platformContainer">
            <div style="height:20px;fontSize:16px;fontWeight:700;">计划状态选择</div>
            <div style="margin-top: 20px">
              <el-radio-group v-model="checkboxGroup" size="small" @change="Selectstatus">
                <el-radio-button v-for="(itam,index) in status" :label="itam.name" :key="index"></el-radio-button>
              </el-radio-group>
            </div>
            <div style="margin-top: 20px">
              <span style="height:20px;fontSize:14px;fontWeight:700;">计划开始时间查询</span>
              <el-date-picker
                v-model="searchDate"
                type="date"
                size='small'
                placeholder="选择日期"
                @change="getBatchTable">
              </el-date-picker>
            </div>
        </div>
        <div class="platformContainer" style="overflow:auto;">
          <div style="height:40px;fontSize:16px;fontWeight:700;">计划列表</div>
              <el-table
                  :data="planTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="multipleTable"
                  @selection-change="handleSelectionChange" 
                  @row-click="TabCurrentChange"
                  style="width: 100%">
                  <el-table-column type="selection"></el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="planTableData.total"
                  :current-page="planTableData.offset"
                  :page-size="planTableData.limit"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange">
                  </el-pagination>
            </div>
        </div>
      </div>
    </el-col>
    <el-col :span='15'>
      <BatchInformation :currentSBatch='currentFBatch' ref='BatchInfo' @refreshBatchTable='getBatchTable'></BatchInformation>
    </el-col>
  </el-row>
</template>

<script>
var moment=require('moment')
import BatchInformation from '@/components/BatchInformatin.vue'
  export default {
    name: "planningScheduling",
    components:{BatchInformation},
    data(){
      return {
        planTableData:{
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        status:[
          {name:"全部"},
          {name:"新增"},
          {name:"待审核"},
          {name:"待下发"},
          {name:"待完成"}, 
          {name:"已完成"}, 
        ],
        checkboxGroup: '全部',
        BrandActive:'',
        mydata:[],
        currentFBatch:{},
        currentBrandName:'',
        multipleSelection:[],
        searchDate:'2020-09-29',//绑定的查询日期
        tableconfig:[{prop:'BatchID',label:"批次号"},{prop:'PlanNum',label:'计划单号'},{prop:'BrandName',label:'品名'},{prop:'PlanStatus',label:'计划状态'}],
      }
    },
    created(){
      this.getBatchTable()
    },
    mounted(){
    },
    methods:{
      getBatchTable(){
        var that=this
        var PlanBeginTime=moment(this.searchDate).format('YYYY-MM-DD')
        var radiovalue = ""
        if(this.checkboxGroup==='全部'){
          radiovalue=''
        }else{
          radiovalue = this.checkboxGroup
        }
        var offset=this.planTableData.offset - 1
        var limit=this.planTableData.limit
        var api="/api/CUID?tableName=PlanManager&PlanStatus="+radiovalue+"&PlanBeginTime="+PlanBeginTime+"&limit="+limit+"&offset="+offset
        this.axios.get(api).then(res => {
          if(res.data.code === "200"){
            var data = res.data.data
            that.planTableData.data = data.rows
            that.planTableData.total = data.total
          }
        },err=>{
           console.log("请求错误")
        })
      },  
      Selectstatus(){
        this.getBatchTable()
      },
      handleSelectionChange(row){
        this.multipleSelection = row
      },
      TabCurrentChange(e){ //点击显示当前的tab行显示详细信息
        this.currentFBatch=e
        this.currentBrandName=e.BrandName
        this.$refs.BatchInfo.getMaterialBom(this.currentBrandName)
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(e)
      },
      handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.getBatchTable()
      },
       handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.getBatchTable()
      }
    }
  }
</script>

<style scoped>

</style>
