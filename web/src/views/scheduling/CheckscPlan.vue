<template>
  <el-row>
    <el-col :span='24'>
       <el-row>
          <el-col :span='24' class="marginBottom">
            <el-button type="primary" size="small" @click="back">返回主流程</el-button>
            <el-button type="primary" size="small" icon='el-icon-refresh-right' @click="refreshData">刷新</el-button>
          </el-col>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">批次列表</div>
              <el-table
                  v-loading="loading"
                  element-loading-text="拼命加载中"
                  element-loading-spinner="el-icon-loading"
                  :data="batchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager"
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                     <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
                     <b class="color-orange" v-else-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-red" v-else-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-lightgreen" v-else-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-purple" v-else-if="scope.row.PlanStatus === '待执行'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-orange" v-else-if="scope.row.PlanStatus === '待备料'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-orange" v-else-if="scope.row.PlanStatus === '物料发送中'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-success" v-else-if="scope.row.PlanStatus === '物料发送完成'">{{ scope.row.PlanStatus }}</b>
                    <b class="color-brown" v-else-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
                    <b class="" v-else>{{ scope.row.PlanStatus }}</b>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width='170'>
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type="success"
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkpass(scope.$index, scope.row)" v-has="['计划审核']">通过</el-button>
                      <el-button
                        size="mini"
                        type="danger"
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkNopass(scope.$index, scope.row)" v-has="['计划审核']">不通过</el-button>
                      <el-button
                        size="mini"
                        v-if="scope.row.PlanStatus==='审核未通过'"
                        @click="searchWhyNopass(scope.$index, scope.row)"
                       >未通过原因
                       </el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="batchTableData.total"
                  :current-page="batchTableData.offset"
                  :page-size="batchTableData.limit"
                  @size-change="batchHandleSizeChange"
                  @current-change="batchHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
       </el-row>
    </el-col>
    <el-col :span='24' class="marginBottom" style="textAlign:right;">
      <el-button type="success" @click="shMultiplebatch" v-has="['计划审核']">多批次审核</el-button>
      <el-button type="primary" v-show="sonstep != 2" @click="sonNextStep">下一步</el-button>
      <el-button type="primary" v-show="sonstep != 0" @click="sonLastStep">上一步</el-button>
      </el-col>
  </el-row>
</template>

<script>
var moment=require('moment')
  export default {
    name: "planningScheduling",
    data(){
      return {
        batchTableData:{ //批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        BrandCode:'',
        BatchID:'',
        blstartBc:'',//备料开始班次
        blendBc:'',//备料结束班次
        blstartTime:'', //备料开始时间
        blendTime:'', //备料结束时间`,
        blSelected:false,
        row:{},
        datalist:[],
        loading:false,
        checkedRow:[],//勾选的原生数组
        batchtableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'SchedulePlanCode',label:'调度编号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'计划产量'},{prop:'Unit',label:'单位'}],//批次列表
      }
    },
    props:['sonNext','sonLast','sonstep'],
    created(){
      this.getPlanManager()
    },
    mounted(){
    },
    methods:{
      sonNextStep(){
        this.$emit('sonNext')
      },
      sonLastStep(){
        this.$emit('sonLast')
      },
      refreshData(){ //刷新数据
        this.getPlanManager()
      },
      back(){ //返回主流程
            this.$router.push('/planProgress')
        },
      searchWhyNopass(index,row){
         this.$alert(row.Description, '原因', {
          confirmButtonText: '知道了',
          callback: action => {
            
          }
        });

      },
      checkpass(index,row){
          var obj=[{
             PlanStatus:'待配置',
             Description:'',
             ID:row.ID
          }]
          var params={
              datalist:JSON.stringify(obj)
            }
          this.$confirm('是否通过该批次审核, 是否继续?', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
               if(res.data.code==='200'){
                 this.$message({
                   type:'success',
                   message:'批次审核成功'
                 })
                 this.getPlanManager()
               }
             })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            });
          });
      },
      checkNopass(index,row){
        var id=row.ID
        this.$prompt('请输入未通过的原因', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType:'text',
        }).then(({ value }) => {
          var params={
            PlanStatus:'审核未通过',
            Describtion:value,
            ID:id
          }
          this.axios.post('/api/checkPlanManagerSingle',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
              this.getPlanManager()
               this.$message({
                type: 'success',
                message: '提交成功'
              });
               this.getPlanManager()
            }else{
                this.$message({
                type: 'error',
                message: '提交失败，请重试'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });       
        });
      },
      getPlanManager(){ //获取批次列表
        this.loading=true
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit,
          PlanStatus:'待审核'
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
          this.loading=false
           if(res.data.code === "200"){
            var data = res.data.data
            this.batchTableData.data = data.rows
            this.batchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      batchHandleSizeChange(limit){ //批次计划 每页条数切换
        this.batchTableData.limit = limit
        this.getPlanManager()
      },
       batchHandleCurrentChange(offset) { //批次计划 页码切换
        this.batchTableData.offset = offset
        this.getPlanManager()
      },
      handleSelectionChangePlanManager(row){ //审核计划批次点击
        this.checkedRow=row
      },
      handleRowClickPlanManager(row){
        this.$refs.batchmultipleTable.toggleRowSelection(row)
      },
      shMultiplebatch(){ //点击多批次下发
        this.datalist=[]
        var flag=true
        if(this.checkedRow.length==0){
          this.$message({
             type:'info',
             message:'请先勾选要下发的批次'
           })
        }else{
          this.checkedRow.forEach((item) => {
            if(item.PlanStatus==='待审核'&& item.BatchID!==""){
              this.datalist.push(item)
            }else{
              flag=false
              this.$message({
                 type:'info',
                 message:'当前所选批次不是待审核状态或者无批次号，请重新选择'
               })
               return;
            }
          })
          if(flag){
            this.datalist=this.datalist.map((item) => {
              return {
                PlanStatus:'待配置',
                Description:'',
                ID:item.ID
                }
            })
            var params={
              datalist:JSON.stringify(this.datalist)
            }
            this.$confirm('是否通过多批次审核, 是否继续?', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
               if(res.data.code==='200'){
                 this.$message({
                   type:'success',
                   message:'多批次审核成功'
                 })
                 this.getPlanManager()
               }
             })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            });
          });
        }}
      },
     
    }
  }
</script>

<style scoped>
  
</style>
