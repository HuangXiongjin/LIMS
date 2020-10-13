<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-18">发送物料明细到WMS</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="sendToWMS">选择计划</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="PlanQuantity" label="批次计划重量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="BrandName" label="品名"></el-table-column>
            <el-table-column prop="BrandType" label="产品类型"></el-table-column>
            <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
            <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
            <el-table-column prop="PlanEndTime" label="计划完成时间"></el-table-column>
            <el-table-column prop="Describtion" label="描述"></el-table-column>
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
          <el-form-item>
            <el-button type="primary" size="small" @click="sendToWMS">发送物料明细</el-button>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-radio-group v-model="radioGroup" size="small" @change="Selectstatus">
              <el-radio-button v-for="(item,index) in status" :label="item.name" :key="index"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleSelectionChangeMaterial" @row-click="handleRowClickMaterial">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="FeedingSeq" label="投料顺序"></el-table-column>
          <el-table-column prop="BucketNum" label="桶号"></el-table-column>
          <el-table-column prop="BucketWeight" label="重量"></el-table-column>
          <el-table-column prop="Flag" label="标识（桶/托盘）"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="Description" label="描述"></el-table-column>
          <el-table-column prop="SendFlag" label="发送WMS标识"></el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
           :total="MaterialTableData.total"
           :current-page="MaterialTableData.offset"
           :page-sizes="[5,10,20]"
           :page-size="MaterialTableData.limit"
           @size-change="handleSizeChangeMaterial"
           @current-change="handleCurrentChangeMaterial">
          </el-pagination>
        </div>
        <el-dialog :title="MaterialTableData.dialogTitle" :visible.sync="MaterialTableData.dialogVisible" width="40%" :append-to-body="true">
          <el-form :model="MaterialTableData.formField" label-width="110px">
            <el-form-item label="投料顺序">
              <el-input v-model="MaterialTableData.formField.FeedingSeq"></el-input>
            </el-form-item>
            <el-form-item label="桶号">
              <el-input v-model="MaterialTableData.formField.BucketNum"></el-input>
            </el-form-item>
            <el-form-item label="重量">
              <el-input v-model="MaterialTableData.formField.BucketWeight"></el-input>
            </el-form-item>
            <el-form-item label="标识（桶/托盘）">
              <el-input v-model="MaterialTableData.formField.Flag"></el-input>
            </el-form-item>
            <el-form-item label="单位">
              <el-input v-model="MaterialTableData.formField.Unit"></el-input>
            </el-form-item>
            <el-form-item label="描述">
              <el-input v-model="MaterialTableData.formField.Description"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="MaterialTableData.dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="save">保 存</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "sendMaterialDetail",
    data(){
      return{
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        MaterialTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            FeedingSeq:"",
            BucketNum:"",
            BucketWeight:"",
            Flag:"",
            Unit:"",
            Description:"",
          },
        },
        status:[
          {name:"待发送"},
          {name:"已发送"},
        ],
        radioGroup:"待发送"
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
          PlanStatus:"待发送物料明细",
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
        this.getMaterialTableData()
      },
      //物料明细
      getMaterialTableData(){
        var that = this
        var params = {
          BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BrandCode,
          SendFlag:this.radioGroup,
          limit:this.MaterialTableData.limit,
          offset:this.MaterialTableData.offset - 1
        }
        this.axios.get("/api/BatchMaterialInfoselect",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MaterialTableData.data = res.data.data.rows
            that.MaterialTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChangeMaterial(limit){ //每页条数切换
        this.MaterialTableData.limit = limit
        this.getMaterialTableData()
      },
      handleCurrentChangeMaterial(offset) { // 页码切换
        this.MaterialTableData.offset = offset
        this.getMaterialTableData()
      },
      handleSelectionChangeMaterial(row){
        this.MaterialTableData.multipleSelection = row
      },
      handleRowClickMaterial(row){
        this.$refs.multipleTableMaterial.toggleRowSelection(row)
      },
      Selectstatus(){
        this.getMaterialTableData()
      },
      sendToWMS(){
        if(this.MaterialTableData.multipleSelection.length > 0){
          var mulId = []
          var params = {}
          this.MaterialTableData.multipleSelection.forEach(item =>{
            mulId.push({id:item.ID});
          })
          params.sendData = JSON.stringify(mulId)
          this.$confirm('确定发送所选计划的物料明细到WMS？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.post("/api/WMS_SendMatils",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "200"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
              }
              this.getMaterialTableData()
            },res =>{
              console.log("请求错误")
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消发送'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: "请选择计划"
          });
        }
      },
      handleForm(label){
        if(label === "添加"){
          if(this.PlanManagerTableData.multipleSelection.length == 1){
            this.MaterialTableData.dialogVisible = true
            this.MaterialTableData.dialogTitle = label
            this.MaterialTableData.formField = {
              FeedingSeq:"",
              BucketNum:"",
              BucketWeight:"",
              Flag:"",
              Unit:"",
              Description:"",
            }
          }else{
            this.$message({
              message: '至少选择一条计划来添加',
              type: 'warning'
            });
          }
        }else if(label === "修改"){
          if(this.MaterialTableData.multipleSelection.length == 1){
            this.MaterialTableData.dialogVisible = true
            this.MaterialTableData.dialogTitle = label
            this.MaterialTableData.formField = {
              FeedingSeq:this.MaterialTableData.multipleSelection[0].FeedingSeq,
              BucketNum:this.MaterialTableData.multipleSelection[0].BucketNum,
              BucketWeight:this.MaterialTableData.multipleSelection[0].BucketWeight,
              Flag:this.MaterialTableData.multipleSelection[0].Flag,
              Unit:this.MaterialTableData.multipleSelection[0].Unit,
              Description:this.MaterialTableData.multipleSelection[0].Description,
            }
          }else{
            this.$message({
              message: '至少选择一条物料明细来修改',
              type: 'warning'
            });
          }
        }else if(label === "删除"){
          var params = {tableName:"Material"}
          var mulId = []
          if(this.MaterialTableData.multipleSelection.length >= 1){
            this.MaterialTableData.multipleSelection.forEach(item =>{
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
                this.getMaterialTableData()
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
        if(this.MaterialTableData.dialogTitle === "添加"){
          var params = {
            tableName:"Material",
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            FeedingSeq:this.MaterialTableData.formField.FeedingSeq,
            BucketNum:this.MaterialTableData.formField.BucketNum,
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Flag:this.MaterialTableData.formField.Flag,
            Unit:this.MaterialTableData.formField.Unit,
            Description:this.MaterialTableData.formField.Description,
            SendFlag:"待发送",
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.MaterialTableData.dialogVisible = false
              this.getMaterialTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }else if(this.MaterialTableData.dialogTitle === "修改"){
          var params = {
            tableName:"Material",
            ID:this.MaterialTableData.multipleSelection[0].ID,
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            FeedingSeq:this.MaterialTableData.formField.FeedingSeq,
            BucketNum:this.MaterialTableData.formField.BucketNum,
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Flag:this.MaterialTableData.formField.Flag,
            Unit:this.MaterialTableData.formField.Unit,
            Description:this.MaterialTableData.formField.Description,
            SendFlag:"待发送",
          }
          this.axios.get("/api/CUID",{
            params:params
          }).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.MaterialTableData.dialogVisible = false
              this.getMaterialTableData()
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
