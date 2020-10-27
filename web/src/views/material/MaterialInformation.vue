<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">物料基础信息</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="handleForm('添加')">添加</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="warning" size="small" @click="handleForm('修改')">修改</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="danger" size="small" @click="handleForm('删除')">删除</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="MATCode" label="物料编码"></el-table-column>
          <el-table-column prop="MATName" label="物料名称"></el-table-column>
          <el-table-column prop="MATType" label="物料类型"></el-table-column>
          <el-table-column prop="Desc" label="物料描述"></el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
           :total="PlanManagerTableData.total"
           :current-page="PlanManagerTableData.offset"
           :page-sizes="[5,10,20]"
           :page-size="PlanManagerTableData.limit"
           @size-change="handleSizeChangePlanManager"
           @current-change="handleCurrentChangePlanManager">
          </el-pagination>
        </div>
        <el-dialog :title="PlanManagerTableData.dialogTitle" :visible.sync="PlanManagerTableData.dialogVisible" width="40%" :append-to-body="true">
          <el-form :model="PlanManagerTableData.formField" label-width="110px">
            <el-form-item label="物料编码">
              <el-input v-model="PlanManagerTableData.formField.MATCode"></el-input>
            </el-form-item>
            <el-form-item label="物料名称">
              <el-input v-model="PlanManagerTableData.formField.MATName"></el-input>
            </el-form-item>
            <el-form-item label="物料类型">
              <el-input v-model="PlanManagerTableData.formField.MATType"></el-input>
            </el-form-item>
            <el-form-item label="物料描述">
              <el-input v-model="PlanManagerTableData.formField.Desc"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="PlanManagerTableData.dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="save">保 存</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    components:{tableView},
    data(){
      return {
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            MATCode:"",
            MATName:"",
            MATType:"",
            Desc:"",
          },
        },
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      //获取物料信息表
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "Material",
          limit:this.PlanManagerTableData.limit,
          offset:this.PlanManagerTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.PlanManagerTableData.data = res.data.data.rows
            that.PlanManagerTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChangePlanManager(limit){ //每页条数切换
        this.PlanManagerTableData.limit = limit
        this.getPlanManagerTableData()
      },
      handleCurrentChangePlanManager(offset) { // 页码切换
        this.PlanManagerTableData.offset = offset
        this.getPlanManagerTableData()
      },
      handleSelectionChangePlanManager(row){
        this.PlanManagerTableData.multipleSelection = row
      },
      handleRowClickPlanManager(row){
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
      },
      Selectstatus(){
        this.getPlanManagerTableData()
      },
      handleForm(label){
        if(label === "添加"){
          this.PlanManagerTableData.dialogVisible = true
          this.PlanManagerTableData.dialogTitle = label
          this.PlanManagerTableData.formField = {
            MATCode:"",
            MATName:"",
            MATType:"",
            Desc:"",
          }
        }else if(label === "修改"){
          if(this.PlanManagerTableData.multipleSelection.length == 1){
            this.PlanManagerTableData.dialogVisible = true
            this.PlanManagerTableData.dialogTitle = label
            this.PlanManagerTableData.formField = {
              MATCode:this.PlanManagerTableData.multipleSelection[0].MATCode,
              MATName:this.PlanManagerTableData.multipleSelection[0].MATName,
              MATType:this.PlanManagerTableData.multipleSelection[0].MATType,
              Desc:this.PlanManagerTableData.multipleSelection[0].Desc,
            }
          }
        }else if(label === "删除"){
          var params = {tableName:"Material"}
          var mulId = []
          if(this.planTableData.multipleSelection.length >= 1){
            this.planTableData.multipleSelection.forEach(item =>{
              mulId.push({id:item.ID});
            })
            params.delete_data = JSON.stringify(mulId)
            this.$confirm('确定删除所选记录？', '提示', {
              distinguishCancelAndClose:true,
              type: 'warning'
            }).then(()  => {
              this.axios.delete("/api/CUID",{
                params: params
              }).then(res =>{
                if(res.data.code === "200"){
                  this.$message({
                    type: 'success',
                    message: res.data.message
                  });
                }
                this.getPlanManagerTableData()
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          }else{
            this.$message({
              message: '至少选择一条数据进行删除',
              type: 'warning'
            });
          }
        }
      },
      save(){
        if(this.PlanManagerTableData.dialogTitle === "添加"){
          var params = {
            tableName:"Material",
            MATCode:this.PlanManagerTableData.formField.MATCode,
            MATName:this.PlanManagerTableData.formField.MATName,
            MATType:this.PlanManagerTableData.formField.MATType,
            Desc:this.PlanManagerTableData.formField.Desc,
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.PlanManagerTableData.dialogVisible = false
              this.getPlanManagerTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }else if(this.PlanManagerTableData.dialogTitle === "修改"){
          var params = {
            tableName:"Material",
            ID:this.PlanManagerTableData.multipleSelection[0].ID,
            MATCode:this.PlanManagerTableData.formField.MATCode,
            MATName:this.PlanManagerTableData.formField.MATName,
            MATType:this.PlanManagerTableData.formField.MATType,
            Desc:this.PlanManagerTableData.formField.Desc,
          }
          this.axios.get("/api/CUID",{
            params:params
          }).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.PlanManagerTableData.dialogVisible = false
              this.getPlanManagerTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }
      },
    }
  }
</script>

<style scoped>

</style>
