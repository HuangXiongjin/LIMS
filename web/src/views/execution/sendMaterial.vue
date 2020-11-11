<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <el-steps :active="steps" finish-status="success" align-center class="marginBottom">
        <el-step title="选择批计划"></el-step>
        <el-step title="录入物料桶/组"></el-step>
        <el-step title="定义每组轮次"></el-step>
        <el-step title="定义每组桶序"></el-step>
        <el-step title="发送物料明细"></el-step>
      </el-steps>
      <el-row v-if="steps == 0">
        <el-col :span="24">
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
            <el-table :data="PlanManagerTableData.data" highlight-current-row border size="small" ref="multipleTablePlanManager" @select="handleSelectPlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
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
        </el-col>
      </el-row>
      <el-row v-if="steps == 1">
        <el-col :span="24">
          <div class="platformContainer">
            <el-form :inline="true">
              <el-form-item>
                <el-button type="info" size="small" @click="addMaterialForm">录入物料</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleMaterialSelectionChange" @row-click="handleMaterialRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="MATName" label="物料名称" width="360"></el-table-column>
              <el-table-column prop="BucketNum" label="桶号"></el-table-column>
              <el-table-column prop="BucketWeight" label="重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
              <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
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
                  <el-select v-model="MaterialTableData.formField.MATName" multiple placeholder="请选择" style="width: 360px;">
                    <el-option
                      v-for="item in MATNameOptions"
                      :key="item.value"
                      :label="item.MATName"
                      :value="item.MATName">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="桶号/组">
                  <el-tag :key="tag" v-for="tag in MaterialTableData.formField.BucketNum" closable :disable-transitions="false" @close="handleClose(tag)">{{tag}}</el-tag>
                  <el-input class="input-new-tag" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm"></el-input>
                  <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 桶号</el-button>
                </el-form-item>
                <el-form-item label="重量/组">
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
      <el-row v-if="steps == 2">
        <el-col :span="24">
          <div class="platformContainer">
            <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleMaterialSelectionChange" @row-click="handleMaterialRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="MATName" label="物料名称" width="360"></el-table-column>
              <el-table-column prop="BucketNum" label="桶号"></el-table-column>
              <el-table-column prop="BucketWeight" label="重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
              <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
              <el-table-column label="操作" fixed="right" width="120">
                <template slot-scope="scope">
                  <el-button size="mini">设置轮次</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
      <el-row v-if="steps == 3">
        <el-col :span="24">
          <div class="platformContainer">
            <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleMaterialSelectionChange" @row-click="handleMaterialRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="MATName" label="物料名称" width="360"></el-table-column>
              <el-table-column prop="BucketNum" label="桶号"></el-table-column>
              <el-table-column prop="BucketWeight" label="重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
              <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
              <el-table-column label="操作" fixed="right" width="120">
                <template slot-scope="scope">
                  <el-button size="mini">设置桶序</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
      <el-row v-if="steps == 4">
        <el-col :span="24">
          <div class="platformContainer">
            <el-table :data="MaterialTableData.data" border size="small" ref="multipleTableMaterial" @selection-change="handleMaterialSelectionChange" @row-click="handleMaterialRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="MATName" label="物料名称" width="360"></el-table-column>
              <el-table-column prop="BucketNum" label="桶号"></el-table-column>
              <el-table-column prop="BucketWeight" label="重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
              <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
              <el-table-column label="操作" fixed="right" width="120">
                <template slot-scope="scope">
                  <el-button size="mini">发送物料明细</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
      <el-col :span="24" style="text-align: right;">
        <el-button type="primary" v-show="steps != 0" @click="lastStep">上一步</el-button>
        <el-button type="primary" v-show="steps != 4" @click="nextStep">下一步</el-button>
        <el-button type="primary" v-show="steps == 4" @click="nextStep">发送物料明细</el-button>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "sendMaterial",
    data(){
      return {
        steps:0,
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
            BucketNum:[],
            BucketWeight:"",
            Unit:"",
            Flag:"",
          },
        },
        UnitData:[],
        MATNameOptions:[],
        inputVisible: false,
        inputValue: ''
      }
    },
    mounted(){
      this.getPlanManagerTableData()
      this.getUnitData()
    },
    methods:{
      nextStep(){
        if(this.steps == 0){
          if(this.PlanManagerTableData.multipleSelection.length == 1){
            this.steps++
            this.getMaterialTableData()
          }else{
            this.$message({
              type: 'info',
              message: "请选择物料需绑定的批计划"
            });
          }
        }else if(this.steps == 4){
          this.sendMaterialInfo()
        }else{
          this.steps++
          this.getMaterialTableData()
        }
      },
      lastStep(){
        this.steps--
      },
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var PlanStatus = ""
        if(this.sendPlanPlanStatus === "待发送"){
          PlanStatus = "已下发"
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
      handleSelectPlanManager(selection,row){  //勾选时只能单选
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.$refs.multipleTablePlanManager.setCurrentRow(row)
      },
      handleRowClickPlanManager(row){
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
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
          BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
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
      handleClose(tag) {
        this.MaterialTableData.formField.BucketNum.splice(this.MaterialTableData.formField.BucketNum.indexOf(tag), 1);
      },
      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },

      handleInputConfirm() {
        let inputValue = this.inputValue;
        if (inputValue) {
          this.MaterialTableData.formField.BucketNum.push(inputValue);
        }
        this.inputVisible = false;
        this.inputValue = '';
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
          this.getBOMData()
        }else{
          this.$message({
            type: 'info',
            message: "请选择物料需绑定的一条批计划"
          });
        }
      },
      EditMaterial(index,row){
        if(row.SendFlag != "WMS已接收"){
          this.MaterialTableData.dialogVisible = true
          this.MaterialTableData.dialogTitle = "编辑"
          this.getBOMData()
          this.MaterialTableData.formField = {
            ID:row.ID,
            BrandCode:row.BrandCode,
            BatchID:row.BatchID,
            MATName:row.MATName.split(","),
            BucketNum:row.BucketNum.split(","),
            BucketWeight:row.BucketWeight,
            Unit:row.Unit,
            Flag:row.Flag,
            EQPCode:row.EQPCode,
            FeedingSeq:row.FeedingSeq,
          }
        }else{
          this.$message({
            type: 'info',
            message: '已发送的物料不可修改'
          });
        }
      },
      DeleteMaterial(index,row){
        if(row.SendFlag != "WMS已接收"){
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
        }else{
          this.$message({
            type: 'info',
            message: '已发送的物料不可删除'
          });
        }
      },
      saveMaterial(){
        if(this.MaterialTableData.dialogTitle === "物料明细录入"){
          var params = {
            tableName:"BatchMaterialInfo",
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
            MATName:this.MaterialTableData.formField.MATName.join(','),
            BucketNum:this.MaterialTableData.formField.BucketNum.join(','),
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Unit:this.MaterialTableData.formField.Unit,
            Flag:this.MaterialTableData.formField.Flag,
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
          var params = {
            tableName:"BatchMaterialInfo",
            ID:this.MaterialTableData.formField.ID,
            BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
            BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
            BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
            MATName:this.MaterialTableData.formField.MATName.join(','),
            BucketNum:this.MaterialTableData.formField.BucketNum.join(','),
            BucketWeight:this.MaterialTableData.formField.BucketWeight,
            Unit:this.MaterialTableData.formField.Unit,
            Flag:this.MaterialTableData.formField.Flag,
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
          var isFlag = true
          this.MaterialTableData.multipleSelection.forEach(item =>{
            if(item.SendFlag === "投料系统已接收"){
              isFlag = false
            }
          })
          if(isFlag){
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
              message: "已发送的物料不能再发送"
            });
          }
        }else{
          this.$message({
            type: 'info',
            message: "请选择物料"
          });
        }
      },
      //确认接收退料
      returnMaterialInfo(){
        if(this.MaterialTableData.multipleSelection.length > 0){
          var isFlag = true
          this.MaterialTableData.multipleSelection.forEach(item =>{
            if(item.SendFlag != "投料系统已接收"){
              isFlag = false
            }
          })
          if(isFlag){
            var mulId = []
            this.MaterialTableData.multipleSelection.forEach(item =>{
              mulId.push({id:item.ID});
            })
            var params = {}
            params.sendData = JSON.stringify(mulId)
            this.$confirm('确定接收已选退料吗？', '提示', {
              distinguishCancelAndClose:true,
              type: 'warning'
            }).then(()  => {
              this.axios.post("/api/WMS_SendReturnMaterialInfo",this.qs.stringify(params)).then(res =>{
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
              message: "只能选择已接收的物料"
            });
          }
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
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>
