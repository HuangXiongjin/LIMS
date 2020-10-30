<template>
  <el-row>
    <el-col :span='24'>
       <el-row>
          <el-col :span='24' class="marginBottom"><el-button type="primary" size="small" @click="back">返回上一步</el-button></el-col>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">批次列表</div>
           <div class="marginBottom"><el-button type="primary" icon="el-icon-folder-checked" size='mini' @click="shMultiplebatch">多批次审核</el-button></div>
              <el-table
                  :data="batchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable"
                  @select='getAllbatchrow'
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width='160'>
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='success'
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkPass(scope.$index, scope.row)">通过</el-button>
                      <el-button
                        size="mini"
                        type="primary"
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkNopass(scope.$index, scope.row)">不通过</el-button>
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
        checkedRow:[],//勾选的原生数组
        batchtableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'每批产量'},{prop:'Unit',label:'单位'}],//批次列表
      }
    },
    created(){
      this.getPlanManager()
    },
    mounted(){
    },
    methods:{
      back(){ //返回上一步
            this.$router.go(-1)
        },
      searchWhyNopass(index,row){
         this.$alert(row.Description, '原因', {
          confirmButtonText: '知道了',
          callback: action => {
            
          }
        });

      },
      checkPass(index,row){
        var id=row.ID
        this.BatchID=row.BatchID
        this.BrandCode=row.BrandCode
        this.$confirm('此操作将审核通过此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'待配置',
            Describtion:'',
            ID:id
          }
          this.axios.post('/api/checkPlanManagerSingle',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
              this.getPlanManager()
               this.$message({
                type: 'success',
                message: '审核成功'
              });
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
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
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
      getAllbatchrow(e){ //审核计划批次点击
        this.checkedRow=e
      },
      shMultiplebatch(){ //点击多批次下发
        this.datalist=[]
        var flag=true
        if(this.checkedRow.length===0){
            this.$message({
               type:'info',
               message:'请先勾选要下发的批次'
             })
             return;
        }else{
          this.checkedRow.forEach((item) => {
          if(item.PlanStatus==='待审核'){
            this.datalist.push(item)
          }else{
            flag=false
            this.$message({
               type:'info',
               message:'当前所选批次包含其他状态，请重新选择'
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
