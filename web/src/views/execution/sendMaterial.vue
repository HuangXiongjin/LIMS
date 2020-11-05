<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16">选择计划，先下方录入物料明细</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="sendMaterialFinish">物料明细发送完成</el-button>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-radio-group v-model="sendPlanPlanStatus" size="small" @change="getPlanManagerTableData">
              <el-radio-button label="待发送"></el-radio-button>
              <el-radio-button label="发送中"></el-radio-button>
              <el-radio-button label="已发送"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
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
            <el-button type="primary" size="small" @click="addMaterialForm">录入物料</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="sendMaterialInfo">发送物料明细</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleMaterialSelectionChange" @row-click="handleMaterialRowClick">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="MATName" label="物料名称"></el-table-column>
          <el-table-column prop="BucketNum" label="桶号"></el-table-column>
          <el-table-column prop="BucketWeight" label="重量"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
          <el-table-column prop="SendFlag" label="发送WMS标识"></el-table-column>
          <el-table-column label="操作" fixed="right" width="150">
            <template slot-scope="scope">
              <el-button size="mini" @click="EditMaterial(scope.$index, scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="DeleteMaterial(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog :title="MaterialTableData.dialogTitle" :visible.sync="MaterialTableData.dialogVisible" width="40%" :append-to-body="true" v-if="MaterialTableData.dialogVisible">
          <el-form :model="MaterialTableData.formField" label-width="110px">
            <el-form-item label="批次号">
              <el-input v-model="PlanManagerTableData.multipleSelection[0].BatchID" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="品名">
              <el-input v-model="PlanManagerTableData.multipleSelection[0].BrandName" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="物料名称">
              <el-select v-model="MaterialTableData.formField.MATName" multiple placeholder="请选择">
                <el-option
                  v-for="item in MATNameOptions"
                  :key="item.value"
                  :label="item.MATName"
                  :value="item.MATName">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="桶号">
              <el-input v-model="MaterialTableData.formField.BucketNum"></el-input>
            </el-form-item>
            <el-form-item label="重量">
              <el-input v-model="MaterialTableData.formField.BucketWeight"></el-input>
            </el-form-item>
            <el-form-item label="单位">
              <el-select v-model="MaterialTableData.formField.Unit" placeholder="请选择">
                <el-option v-for="(item,index) in UnitData" :key="index" :label="item.UnitValue" :value="item.UnitValue"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="桶/托盘标识">
              <el-select v-model="MaterialTableData.formField.Flag" placeholder="请选择">
                <el-option label="桶" value="桶"></el-option>
                <el-option label="托盘" value="托盘"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="MaterialTableData.dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="saveMaterial">保 存</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "sendMaterial",
    data(){
      return {
        sendPlanPlanStatus:"待发送",
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        MaterialTableData:{
          data:[],
          multipleSelection: [],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            ID:"",
            MATName:[],
            BucketNum:"",
            BucketWeight:"",
            Unit:"",
            Flag:"",
          },
        },
        UnitData:[],
        MATNameOptions:[],
      }
    },
    mounted(){
      this.getPlanManagerTableData()
      this.getBOMData()
      this.getUnitData()
    },
    methods:{
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var PlanStatus = ""
        if(this.sendPlanPlanStatus === "待发送"){
          PlanStatus = "已发送投料计划"
        }else if(this.sendPlanPlanStatus === "发送中"){
          PlanStatus = "物料发送中"
        }else if(this.sendPlanPlanStatus === "已发送"){
          PlanStatus = "物料发送完成"
        }
        var params = {
          tableName: "PlanManager",
          PlanStatus:PlanStatus,
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
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.getMaterialTableData()
      },
      //发送物料明细完成
      sendMaterialFinish(){
        if(this.PlanManagerTableData.multipleSelection.length == 1){
          var params = {
            sendData:"",
            PlanStatus:"物料发送完成",
            PlanID:this.PlanManagerTableData.multipleSelection[0].ID
          }
          this.$confirm('确定完成发送此批的物料明细吗？', '提示', {
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
              message: '已取消操作'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: "请选择需完成发送物料的批计划"
          });
        }
      },
      //获取单位
      getUnitData(){
        var that = this
        var params = {
          tableName: "Unit",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.UnitData = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //获取物料BOM
      getBOMData(){
        var that = this
        var params = {
          tableName: "MaterialBOM",
          BrandName:this.PlanManagerTableData.multipleSelection.BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MATNameOptions = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //查询物料明细-录入
      getMaterialTableData(){
        var that = this
        var params = {
          tableName: "BatchMaterialInfo",
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MaterialTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleMaterialSelectionChange(row){
        this.MaterialTableData.multipleSelection = row
      },
      handleMaterialRowClick(row){
        this.$refs.multipleTableMaterial.toggleRowSelection(row)
      },
      addMaterialForm(){
        if(this.PlanManagerTableData.multipleSelection.length == 1){
          this.MaterialTableData.dialogVisible = true
          this.MaterialTableData.dialogTitle = "物料明细录入"
          this.getTiQuEquipment()
        }else{
          this.$message({
            type: 'info',
            message: "请选择物料需绑定的一条批计划"
          });
        }
      },
      getTiQuEquipment(){
        this.TLEQList = []
        var params = {
          ID:this.PlanManagerTableData.multipleSelection[0].ID,
        }
        this.axios.get("/api/selectTiQuEquipment",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            this.TLEQList = res.data.data
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      EditMaterial(index,row){
        this.MaterialTableData.dialogVisible = true
        this.MaterialTableData.dialogTitle = "编辑"
        this.getTiQuEquipment()
        this.MaterialTableData.formField = {
          ID:row.ID,
          BrandCode:row.BrandCode,
          BatchID:row.BatchID,
          MATName:row.MATName.split(","),
          BucketNum:row.BucketNum,
          BucketWeight:row.BucketWeight,
          Unit:row.Unit,
          Flag:row.Flag,
          EQPCode:row.EQPCode,
          FeedingSeq:row.FeedingSeq,
        }
      },
      DeleteMaterial(index,row){
        var params = {tableName:"BatchMaterialInfo"}
        var mulId = []
        mulId.push({
          id:row.ID
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
      },
      saveMaterial(){
        if(this.MaterialTableData.dialogTitle === "物料明细录入"){
          if(this.MaterialTableData.formField.EQPCode){
            this.TLEQList.forEach(item =>{
              if(item.EQPCode === this.MaterialTableData.formField.EQPCode){
                this.MaterialTableData.formField.EQPName = item.EQPName
              }
            })
          }
          var params = {
            tableName:"BatchMaterialInfo",
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
            MATName:this.MaterialTableData.formField.MATName.join(','),
            BucketNum:this.MaterialTableData.formField.BucketNum,
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Unit:this.MaterialTableData.formField.Unit,
            Flag:this.MaterialTableData.formField.Flag,
            EQPCode:this.MaterialTableData.formField.EQPCode,
            EQPName:this.MaterialTableData.formField.EQPName,
            FeedingSeq:this.MaterialTableData.formField.FeedingSeq,
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
        }else if(this.MaterialTableData.dialogTitle === "编辑"){
          if(this.MaterialTableData.formField.EQPCode){
            this.TLEQList.forEach(item =>{
              if(item.EQPCode === this.MaterialTableData.formField.EQPCode){
                this.MaterialTableData.formField.EQPName = item.EQPName
              }
            })
          }
          var params = {
            tableName:"BatchMaterialInfo",
            ID:this.MaterialTableData.formField.ID,
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
            MATName:this.MaterialTableData.formField.MATName.join(','),
            BucketNum:this.MaterialTableData.formField.BucketNum,
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Unit:this.MaterialTableData.formField.Unit,
            Flag:this.MaterialTableData.formField.Flag,
            EQPCode:this.MaterialTableData.formField.EQPCode,
            EQPName:this.MaterialTableData.formField.EQPName,
            FeedingSeq:this.MaterialTableData.formField.FeedingSeq
          }
          this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
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
      //发送物料明细到WMS
      sendMaterialInfo(){
        if(this.MaterialTableData.multipleSelection.length > 0){
          var mulId = []
          this.MaterialTableData.multipleSelection.forEach(item =>{
            mulId.push({id:item.ID});
          })
          var params = {}
          params.sendData = JSON.stringify(mulId)
          params.PlanStatus = "物料发送中"
          params.PlanID = this.PlanManagerTableData.multipleSelection[0].ID
          this.$confirm('确定发送此批的物料明细到WMS吗？', '提示', {
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
            message: "请选择物料"
          });
        }
      },
    }
  }
</script>

<style scoped>

</style>
