<template>
    <el-row>
           <el-col :span='24' class="marginBottom"><el-button type="primary" size="small" @click="back">返回主流程</el-button></el-col>
           <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">待下发列表</div>
           <el-button type="success" icon="el-icon-position" size='mini' @click="distributemulBatch" class="marginBottom">下发</el-button>
              <el-table
                  :data="eqlistTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  @select='getAllbatchrow'
                  ref="eqlistmultipleTable"
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in eqlistableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-brown" v-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width='100'>
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type="primary"
                        @click="chPlan(scope.$index, scope.row)">撤回</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="eqlistTableData.total"
                  :current-page="eqlistTableData.offset"
                  :page-size="eqlistTableData.limit"
                  @size-change="eqlistHandleSizeChange"
                  @current-change="eqlistHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
           <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">已下发列表</div>
              <el-table
                  :data="yxfbatchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref='dxfTable'
                  @row-click='yxfClick'
                  @select='yxfSelect'
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in eqlistableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-brown" v-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="yxfbatchTableData.total"
                  :current-page="yxfbatchTableData.offset"
                  :page-size="yxfbatchTableData.limit"
                  @size-change="yxfbatchHandleSizeChange"
                  @current-change="yxfbatchHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
       </el-row>
</template>
<script>
export default {
    data(){
        return {
        eqlistTableData:{ //下发批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        yxfbatchTableData:{ //下发批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        checkedRow:[],
        datalist:[],
        eqlistableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'SchedulePlanCode',label:'调度编号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'计划产量'},{prop:'Unit',label:'单位'}],//选择设备列表
      }

    },
    created(){
        this.getSelectedEq()
        this.getYxfBatch()
    },
    methods: {
      distributemulBatch(){
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
          if(item.PlanStatus==='待下发'){
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
          return item.ID
        })
        var params={
          PlanStatus:'已下发',
          IDs:JSON.stringify(this.datalist)
        }
        this.$confirm('是否下发勾选的批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
           if(res.data.code==='200'){
             this.$message({
               type:'success',
               message:'勾选批次下发成功'
             })
            this.getSelectedEq()
            this.getYxfBatch()
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
        getAllbatchrow(e,row){
          this.checkedRow=e
          this.$refs.eqlistmultipleTable.setCurrentRow(row)
        },
        back(){ //返回主流程
          this.$router.push('/planProgress')
        },
        yxfbatchHandleSizeChange(limit){ //已选设备 每页条数切换
        this.yxfbatchTableData.limit = limit
        this.getYxfBatch()
      },
       yxfbatchHandleCurrentChange(offset) { //已选设备 页码切换
        this.yxfbatchTableData.offset = offset
        this.getYxfBatch()
      },
       eqlistHandleSizeChange(limit){ //已选设备 每页条数切换
        this.eqlistTableData.limit = limit
        this.getSelectedEq()
      },
       eqlistHandleCurrentChange(offset) { //已选设备 页码切换
        this.eqlistTableData.offset = offset
        this.getSelectedEq()
      },
      chPlan(index,row){
        var id=row.ID
        var params={
          PlanStatus:'撤回',
          ID:id
        }
        this.$confirm('此操作将撤回此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
            this.getSelectedEq()
            this.$message({
              type:'success',
              message:res.data.message
            })
          }else{
            this.$message({
              type:'error',
              message:'撤回失败,请重试'
            })
          }
        })},()=>{
           this.$message({
              type:'info',
              message:'已取消操作'
            })
        })
      },
       getSelectedEq(){    //  查询完成设备选择的批次信息
        var params={
          tableName:this.eqlistTableData.tableName,
          PlanStatus:'待下发',
          offset:this.eqlistTableData.offset-1,
          limit:this.eqlistTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.eqlistTableData.data = data.rows
            this.eqlistTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      getYxfBatch(){
        var params={
          tableName:'PlanManager',
          PlanStatus:'已下发',
          offset:this.yxfbatchTableData.offset-1,
          limit:this.yxfbatchTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.yxfbatchTableData.data = data.rows
            this.yxfbatchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })

      },
      yxfClick(row){
        this.$refs.dxfTable.clearSelection()
        this.$refs.dxfTable.toggleRowSelection(row)
      },
      yxfSelect(e,row){
        this.$refs.dxfTable.clearSelection()
        this.$refs.dxfTable.toggleRowSelection(row)
        this.$refs.dxfTable.setCurrentRow(row)
      }
    }
}
</script>
<style scoped>
    
</style>>