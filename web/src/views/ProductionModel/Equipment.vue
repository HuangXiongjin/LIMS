<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title"><span>生产设备定义</span></div>
      <div>
          <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in Processtab" :key="index" v-bind:effect="item.PUName===PUName?'dark':'plain'" @click="getCurrentprocess(item.PUName,item.PUCode,item.ID)">{{item.PUName}}</el-tag>
      </div>
      <div class='platformContainer marginTop'>
          <el-form :inline="true" v-has="['生产建模']">
              <el-form-item v-for='(item,index) in handleType' :key='index'>
                <el-button :type='item.type' @click='MakeOperation(item.label)' size='small'>{{item.label}}</el-button>
              </el-form-item>
          </el-form>
          <el-table border :data="tableData" size='small' @selection-change="handleSelectionChange">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
              <el-table-column prop="Number" label="设备编号"></el-table-column>
              <el-table-column prop="EQPName" label="设备名称"></el-table-column>
              <el-table-column prop="Desc" label="描述"></el-table-column>
          </el-table>
      </div>
      <el-dialog :title="OperationName" :visible.sync="dialogVisible" :close-on-click-modal="false" :append-to-body="true" width="40%">
              <el-form :model="submitForm" label-width="110px">
                <el-form-item label="设备编码">
                   <el-input v-model="submitForm.EQPCode"></el-input>
                </el-form-item>
                <el-form-item label="设备编号">
                   <el-input v-model="submitForm.Number"></el-input>
                </el-form-item>
                <el-form-item label="设备名称">
                   <el-input v-model="submitForm.EQPName"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                   <el-input v-model="submitForm.Desc"></el-input>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="save" :disabled='addloading'>保存</el-button>
              </div>
          </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "Equipment",
    data(){
      return {
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
        PUCode:'',
        PUName:'',
        multipleSelection:[],
        OperationName:'',
        submitForm:{
          EQPCode:'',
          EQPName:'',
          Number:'',
          Desc:''
        },
        dialogVisible:false,
        Processtab:[], //提取工艺
        radio1:'',
        tableData: [],
        addloading:false
      }
    },
    created(){
      this.getProcessTab()
    },
    methods:{
      getProcessTab(){
        var params={
          tableName:'ProcessUnit'
        }
      this.axios.get('/api/CUID',{params:params}).then(res=>{
        this.Processtab=res.data.data.rows //提取
      })
      },
      getCurrentprocess(name,code,id){ //点击展示对应的流程工艺
        this.PUName=name
        this.PUCode=code
        this.Searcheq()
      },
      MakeOperation(e){ //点击进行设备的增删查改
          this.OperationName=e
         if(this.OperationName==='添加'){
          if(this.PUName===''){
             this.$message({
                type: 'error',
                message: '请选择工艺段进行添加'
              });
              return;
          }
          this.dialogVisible=true
        }else if(this.OperationName==='修改'){
           if(this.multipleSelection.length == 1){
            this.dialogVisible=true
            this.submitForm = {
              EQPCode:this.multipleSelection[0].EQPCode,
              Number:this.multipleSelection[0].Number,
              EQPName:this.multipleSelection[0].EQPName,
              Desc:this.multipleSelection[0].Desc,
            }
          }else{
            this.$message({
              type: 'info',
              message: "请选择一项工艺段设备"
            });
          }
        }else if(this.OperationName==='删除'){
          var params = {tableName:"ProductEquipment"}
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
                this.Searcheq()
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
        if(this.OperationName === "添加"){
          this.addloading=true
          var params = {
            tableName:"ProductEquipment",
            EQPCode:this.submitForm.EQPCode,
            Number:this.submitForm.Number,
            EQPName:this.submitForm.EQPName,
            PUCode:this.PUCode,
            PUName:this.PUName,
            Desc:this.submitForm.Desc,
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            this.addloading=false
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.dialogVisible = false
              this.Searcheq()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
            this.addloading=false
          })
        }else if(this.OperationName === "修改"){
          var params = {
            tableName:"ProductEquipment",
            ID:this.multipleSelection[0].ID,
            EQPCode:this.submitForm.EQPCode,
            Number:this.submitForm.Number,
            EQPName:this.submitForm.EQPName,
            Desc:this.submitForm.Desc,
            PUName:this.PUName,
            PUCode:this.PUCode,
          }
          this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.dialogVisible = false
              this.Searcheq()
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
      handleSelectionChange(row){
        this.multipleSelection = row
      },
      Searcheq(){
        var params={
          tableName:'ProductEquipment',
          PUName:this.PUName
        }
        this.axios.get("/api/CUID",{params: params}).then(res => {
          if(res.data.code === "200"){
            this.tableData = res.data.data.rows
          }else{
            this.$message({
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
