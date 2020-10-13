<template>
    <div class="platformContainer">
        <el-row>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">计划进度</div></el-col>
          <el-col :span='24' class="marginBottom">
            <el-steps :active="currentstep" align-center process-status='finish'>
                <el-step  v-for="(item,index) in steps" :title="item.title" :key='index'>
                </el-step>
             </el-steps>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;marginTop:25px;">计划详情</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
            <el-row>
              <el-col :span='3'>
                <div style="paddingBottom:14px;">计划单号</div>
                <div>{{currentSBatch.PlanNum}}</div>
              </el-col>
              <el-col :span='13'>
                 <div style="paddingBottom:14px;">状态</div>
                <div>{{currentSBatch.PlanStatus}}</div>
              </el-col>
              <el-col :span='4' v-if="currentSBatch.PlanStatus==='待审核'"><el-button type="success" plain @click="CheckPass">审核计划</el-button></el-col>
              <el-col :span='4' v-if="currentSBatch.PlanStatus==='待审核'"><el-button type="warning" plain @click='CheckNopass'>审核未通过</el-button></el-col>
              <el-col :span='4' v-if="currentSBatch.PlanStatus==='待下发'"><el-button type="warning" plain @click='Backstep'>撤回</el-button></el-col>
              <el-col :span='4' v-if="currentSBatch.PlanStatus==='待下发'"><el-button type="success" plain @click='Makingplan'>下发计划</el-button></el-col>
            </el-row>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">基础信息</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
             <el-table
              :data="[currentSBatch]"
              size='small'
              style="width: 100%">
             <el-table-column v-for="item in tableconfig" :width='item.width'  :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
            </el-table>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">物料BOM</div></el-col>
          <el-col :span='24' class="marginBottom">
            <div class="marginBottom">
               <el-table
                  :data="materialbom.data"
                  size='small'
                  highlight-current-row
                  @row-click="ClickCurrentTab"
                  style="width: 100%">
                  <el-table-column v-for="item in materialbomtable" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
                 <div class="paginationClass">
                  <el-pagination background  layout="total, prev, pager, next, jumper"
                  :total="materialbom.total"
                  :current-page="materialbom.offset"
                  :page-size="materialbom.limit"
                  @current-change="mbhandleCurrentChange">
                  </el-pagination>
            </div>
            </div>
            <div style="fontSize:16px;fontWeight:700;" class="marginBottom">物料明细</div>
            <div class="marginBottom">
               <el-table
                  :data="materialinfobom.data"
                  size='small'
                  style="width: 100%">
                  <el-table-column v-for="item in materialinfotable" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
                 <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="materialinfobom.total"
                  :current-page="materialinfobom.offset"
                  :page-size="materialinfobom.limit"
                  @current-change="mihandleCurrentChange">
                  </el-pagination>
            </div>
            </div>
          </el-col>
        </el-row>
      </div>
</template>
<script>
import qs from 'qs'
export default {
    props:['currentSBatch'],
    data(){
        return {
            currentMaterial:'',
            currentstep:0,
            materialbom:{ //物料BOM
                tableName:"MaterialBOM",
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            materialinfobom:{ //物料明细表
                tableName:"Material",
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            steps:[{title:'新增'},{title:'待审核'},{title:'待下发'},{title:'待完成'},{title:'已完成'}],
            tableconfig:[{prop:'BatchID',label:"批次号",width:'100'},{prop:'BrandName',label:'品名',width:'90'},{prop:'PlanStatus',label:'计划状态',width:'110'},{prop:'PlanBeginTime',label:'计划开始时间'},{prop:'PlanEndTime',label:'计划完成时间'}],
            materialbomtable:[{prop:'MATCode',label:"物料编码"},{prop:'MATName',label:'物料名称'},{prop:'BatchPercentage',label:'百分比'},{prop:'BatchSingleMATWeight',label:'投料单一重量'},{prop:'BatchTotalWeight',label:'投料批总重量'}],
            materialinfotable:[{prop:'MATCode',label:"物料编码"},{prop:'MATName',label:'物料名称'},{prop:'Desc',label:'物料描述'},{prop:'MATTypeID',label:'物料类型ID'},{prop:'MATBatchNo',label:'物料标识'}],

        }
    },
    watch: {
      "currentSBatch.PlanStatus":function (newValue, oldValue) { //监听传递的状态
       if(newValue==='新增'){
         this.currentstep=0
       }else if(newValue==='待审核'){
         this.currentstep=1
       }else if(newValue==='待下发'){
         this.currentstep=2
       }else if(newValue==='待完成'){
         this.currentstep=3
      }else if(newValue==='已完成'){
         this.currentstep=4
      }
      }
    },
    methods:{
      Makingplan(){ //下发计划
        this.$confirm('是否确定下发计划?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'已下发',
            ID:this.currentSBatch.ID
          }
          this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: res.data.message
              });
              this.$emit('refreshBatchTable')
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      },
      Backstep(){ //下发撤回
        this.$confirm('确定撤回下发?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'撤回',
            ID:this.currentSBatch.ID
          }
          this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: res.data.message
              });
               this.$emit('refreshBatchTable')
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      },
      CheckPass(){ //审核通过
         this.$confirm('此操作将审核通过此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'待下发',
            Describtion:'',
            ID:this.currentSBatch.ID
          }
          this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: '审核成功'
              });
               this.$emit('refreshBatchTable')
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      },
      CheckNopass(){ //审核未通过
        this.$prompt('请输入未通过的原因', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType:'text',
        }).then(({ value }) => {
          var params={
            PlanStatus:'审核未通过',
            Describtion:value,
            ID:this.currentSBatch.ID
          }
          this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: '提交成功'
              });
               this.$emit('refreshBatchTable')
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
       getMaterialBom(BrandName){ //查询当前品名物料BOM
        var that = this
        var params = {
          tableName: this.materialbom.tableName,
          field:"BrandName",
          fieldvalue:BrandName,
          limit:this.materialbom.limit,
          offset:this.materialbom.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.materialbom.data = res.data.data.rows
            that.materialbom.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      ClickCurrentTab(e){
        this.currentMaterial=e.MATName
        this.getMaterialInfo(this.currentMaterial)
      },
       getMaterialInfo(materialname){ //查询当前品名物料详情信息
        var that = this
        var params = {
          tableName: this.materialinfobom.tableName,
          field:"MATName",
          fieldvalue:materialname,//当前点击的物料名称
          limit:this.materialinfobom.limit,
          offset:this.materialinfobom.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.materialinfobom.data = res.data.data.rows
            that.materialinfobom.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
       mbhandleCurrentChange(offset) { // 物料BOM页码切换
        this.materialbom.offset = offset
        this.getMaterialBom(this.currentSBatch.BrandName)
      },
       mihandleCurrentChange(offset) { // 物料详情页码切换
        this.materialinfobom.offset = offset
        this.getMaterialInfo(this.currentMaterial)
      },
    }
}
</script>
<style scoped>

</style>