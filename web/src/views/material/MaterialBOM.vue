<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span>物料BOM</span>
      </div>
      <el-row :gutter="15">
        <el-col :span="4">
          <div class="platformContainer">
            <p class="marginBottom">选择要维护BOM的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
        </el-col>
        <el-col :span="20">
          <div class="platformContainer">
            <p class="marginBottom">{{ BrandActive }}表格数据</p>
            <el-form :inline="true" v-has="['生产建模']">
              <el-form-item v-for="(item,index) in handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleForm(item.label)">{{ item.label }}</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="BOMList" border size="small" ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="MATCode" label="物料编码"></el-table-column>
              <el-table-column prop="MATName" label="物料名称"></el-table-column>
              <el-table-column prop="BatchTotalWeight" label="投料批总重量"></el-table-column>
              <el-table-column prop="BatchSingleMATWeight" label="投料单一物料重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="BatchPercentage" label="百分比"></el-table-column>
              <el-table-column prop="Grade" label="等级"></el-table-column>
            </el-table>
            <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="formField" label-width="110px">
                <el-form-item label="物料编码">
                  <el-input v-model="formField.MATCode"></el-input>
                </el-form-item>
                <el-form-item label="物料名称">
                  <el-input v-model="formField.MATName"></el-input>
                </el-form-item>
                <el-form-item label="投料批总重量">
                  <el-input v-model="formField.BatchTotalWeight"></el-input>
                </el-form-item>
                <el-form-item label="投料单一物料重量">
                  <el-input v-model="formField.BatchSingleMATWeight"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                  <el-select v-model="formField.Unit" placeholder="请选择">
                    <el-option v-for="(item,index) in UnitTableData" :key="index" :label="item.UnitValue" :value="item.UnitValue"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="百分比">
                  <el-input v-model="formField.BatchPercentage"></el-input>
                </el-form-item>
                <el-form-item label="等级">
                  <el-input v-model="formField.Grade"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="save" :disabled="addloading">保 存</el-button>
              </span>
            </el-dialog>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"MaterialBOM",
    data(){
      return {
        productName:"",
        results:[],
        scheduleTableData:[],
        BrandActive:"",
        BrandCode:"",
        BOMList:[],
        multipleSelection:[],
        handleType:[
          {type:"primary",label:"添加"},
          {type:"warning",label:"修改"},
          {type:"danger",label:"删除"},
        ],
        dialogVisible:false,
        dialogTitle:"",
        formField:{
          MATCode:"",
          MATName:"",
          BatchTotalWeight:"",
          BatchSingleMATWeight:"",
          Unit:"",
          BatchPercentage:"",
          Grade:"",
        },
        addloading:false,
        UnitTableData:[],
      }
    },
    created(){
      this.getUnitTableData()
      this.getScheduleTableData()
    },
    methods:{
      getUnitTableData(){ //获取单位
        var that = this
        var params = {
          tableName: "Unit",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.UnitTableData = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getScheduleTableData(){ //获取品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.scheduleTableData = res.data.data.rows
            that.results = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleChangeProductName(queryString){
        if(queryString != ""){
          this.results = this.scheduleTableData.filter((string) =>{
            return Object.keys(string).some(function(key) {
              return String(string[key]).toLowerCase().indexOf(queryString) > -1
            })
          })
        }else{
          this.results = this.scheduleTableData
        }
      },
      clickBrandTag(BrandName,BrandCode){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.getBOMTable(BrandName)
      },
      getBOMTable(BrandName){
        var that = this
        var params = {
          tableName: "MaterialBOM",
          BrandName:BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.BOMList = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSelectionChange(row){
        this.multipleSelection = row
      },
      handleRowClick(row){
        this.$refs.multipleTable.toggleRowSelection(row)
      },
      handleForm(label){
        if(label === "添加"){
          if(this.BrandActive){
            this.dialogVisible = true
            this.dialogTitle = label
          }else{
            this.$message({
              type: 'info',
              message: '请选择品名'
            });
          }
        }else if(label === "修改"){
          if(this.multipleSelection.length == 1){
            this.dialogVisible = true
            this.dialogTitle = label
            this.formField = {
              MATCode:this.multipleSelection[0].MATCode,
              MATName:this.multipleSelection[0].MATName,
              BatchTotalWeight:this.multipleSelection[0].BatchTotalWeight,
              BatchSingleMATWeight:this.multipleSelection[0].BatchSingleMATWeight,
              Unit:this.multipleSelection[0].Unit,
              BatchPercentage:this.multipleSelection[0].BatchPercentage,
              Grade:this.multipleSelection[0].Grade,
            }
          }else{
            this.$message({
              type: 'info',
              message: "请单选一条物料信息"
            });
          }
        }else if(label === "删除"){
          var params = {tableName:"MaterialBOM"}
          var mulId = []
          if(this.multipleSelection.length >= 1){
            this.multipleSelection.forEach(item =>{
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
                this.getBOMTable(this.BrandActive)
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
        if(this.dialogTitle === "添加"){
          this.addloading= true
          var params = {
            tableName:"MaterialBOM",
            MATCode:this.formField.MATCode,
            MATName:this.formField.MATName,
            BatchTotalWeight:this.formField.BatchTotalWeight,
            BatchSingleMATWeight:this.formField.BatchSingleMATWeight,
            Unit:this.formField.Unit,
            BatchPercentage:this.formField.BatchPercentage,
            Grade:this.formField.Grade,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            this.addloading= false
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.dialogVisible = false
              this.getBOMTable(this.BrandActive)
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
            this.addloading= false
          })
        }else if(this.dialogTitle === "修改"){
          var params = {
            tableName:"MaterialBOM",
            ID:this.multipleSelection[0].ID,
            MATCode:this.formField.MATCode,
            MATName:this.formField.MATName,
            BatchTotalWeight:this.formField.BatchTotalWeight,
            BatchSingleMATWeight:this.formField.BatchSingleMATWeight,
            Unit:this.formField.Unit,
            BatchPercentage:this.formField.BatchPercentage,
            Grade:this.formField.Grade,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
          }
          this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.dialogVisible = false
              this.getBOMTable(this.BrandActive)
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
      }
    }
  }
</script>

<style scoped>

</style>
