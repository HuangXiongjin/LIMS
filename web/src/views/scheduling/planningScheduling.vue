<template>
  <el-row :gutter='20'>
    <el-col :span='9'>
      <div>
        <div class="platformContainer" style="height:124px;">
          <div style="height:30px;lineHeight:30px;fontSize:16px;fontWeight:700;">计划明细</div>
            <div style="height:60px;lineHeight:70px;">
              <div style="display:inline-block;width:45%;">
                <div><span style="marginRight:15px;">当日计划数量</span><span>5批</span></div>
              </div>
              <div style="display:inline-block;width:45%;">
                <div><span style="marginRight:15px;">待处理计划数量</span><span>4批</span></div>
              </div>
            </div>
        </div>
        <div class="platformContainer" style="height:600px;overflow:auto;">
          <div style="height:40px;borderBottom:1px solid #ccc;fontSize:16px;fontWeight:700;">计划列表</div>
              <el-table
                  :data="sidetableData"
                  highlight-current-row
                  @row-click="TabCurrentChange"
                  style="width: 100%">
                   <el-table-column
                    type="index"
                    width="40">
                  </el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
                  :total="planTableData.total"
                  :current-page="planTableData.offset"
                  :page-sizes="[5,10,20]"
                  :page-size="planTableData.limit"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange">
                  </el-pagination>
            </div>
        </div>
      </div>
    </el-col>
    <el-col :span='15'>
      <BatchInformation :currentSBatch='currentFBatch'></BatchInformation>
    </el-col>
  </el-row>
</template>

<script>
import BatchInformation from '@/components/BatchInformatin.vue'
  export default {
    name: "planningScheduling",
    components:{BatchInformation},
    data(){
      return {
          planTableData:{
            tableName:"PlanManager",
            data:[],
            limit: 5,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
         BrandActive:'',
         sidetableData: [{
            BatchID:'LPL20200825H',
            BrandName:'黄皮',
            PlanStatus: '待执行',
            PlanBeginTime: '2016-05-02 08:00:00',
            PlanEndTime: '2016-05-02 08:00:00',
            PlanNum:'HP002456'
          },{
            BatchID:'LPL20200825H',
            BrandName:'黄芪',
            PlanStatus: '待执行',
            PlanBeginTime: '2016-06-02 18:00:00',
            PlanEndTime: '2016-06-02 18:15:00',
            PlanNum:'HQ003145'
          },{
            BatchID:'LPL20200825H',
            BrandName:'白芍',
            PlanStatus: '待执行',
            PlanBeginTime: '2016-05-04 03:00:00',
            PlanEndTime: '2016-05-04 14:00:00',
            PlanNum:'BS007895'
          },
          {
            BatchID:'LPL20200825H',
            BrandName:'花椒',
            PlanStatus: '待执行',
            PlanBeginTime: '2016-05-10 08:00:00',
            PlanEndTime: '2016-05-12 18:00:00',
            PlanNum:'HJ00675'
          },
          {
            BatchID:'LPL20200825H',
            BrandName:'陈皮',
            PlanStatus: '待执行',
            PlanBeginTime: '2016-05-02 08:00:00',
            PlanEndTime: '2016-05-02 08:00:00',
            PlanNum:'CP440455'
          }],
          mydata:[],
          currentFBatch:{},
          steps:[{title:'计划申请',decription:'开始时间 2020-09-10'},{title:'计划申请',decription:'开始时间 2020-09-10'},{title:'计划申请',decription:'开始时间 2020-09-10'}],
          tableconfig:[{prop:'BatchID',label:"批次号",width:'90'},{prop:'BrandName',label:'品名',width:'100'},{prop:'PlanStatus',label:'计划状态',width:'90'},{prop:'PlanBeginTime',label:'计划开始时间',width:'190'},{prop:'PlanEndTime',label:'计划完成时间',width:'190'},{prop:'PlanNum',label:'计划单号',width:90}],
      }
    },
    created(){
      this.getBatchTable()
    },
    mounted(){
    },
    methods:{
      getBatchTable(){ //初始化获取表的内容
        var that = this
        var params = {
          tableName: this.planTableData.tableName,
          limit:this.planTableData.limit,
          offset:this.planTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.planTableData.data = data.rows
            that.planTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      TabCurrentChange(e){ //点击显示当前的tab行显示详细信息
        this.currentFBatch=e
      },
      handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.getBatchTable()
      },
       handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.getBatchTable()
      },
      getPlanTableData(BrandName){ //查询当前计划单号
        var that = this
        var params = {
          tableName: "product_plan",
          field:"BrandName",
          fieldvalue:BrandName,
          limit:this.planTableData.limit,
          offset:this.planTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.planTableData.data = res.data.data.rows
            that.planTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
