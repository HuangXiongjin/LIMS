<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step @click.native="clickStep(0)" class="cursor-pointer" title="批次计划信息"></el-step>
        <el-step @click.native="clickStep(1)" class="cursor-pointer" title="分配工艺设备"></el-step>
        <el-step @click.native="clickStep(2)" class="cursor-pointer" title="其他日程"></el-step>
        <el-step @click.native="clickStep(3)" class="cursor-pointer" title="批计划排产"></el-step>
      </el-steps>
      <el-row :gutter="15">
        <el-col :span="24" v-if="steps == 0">
          <el-col :span="6">
            <div class="platformContainer">
              <p class="marginBottom">请根据品名查询计划</p>
              <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
              <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in scheduleList" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
            </div>
          </el-col>
          <el-col :span="18">
            <div class="platformContainer">
              <p class="marginBottom">当前选择的是{{ BrandActive }}</p>
              <el-form :inline="true">
                <el-form-item v-for="(item,index) in handleType" :key="index">
                  <el-button :type="item.type" size="small" @click="handleForm(item.label)">{{ item.label }}</el-button>
                </el-form-item>
              </el-form>
              <el-table :data="tableData" border size="small" @selection-change="handleSelectionChange">
                <el-table-column type="selection"></el-table-column>
                <el-table-column prop="BatchID" label="批次号"></el-table-column>
                <el-table-column prop="PlanQuantity" label="计划成品重量"></el-table-column>
                <el-table-column prop="Unit" label="单位"></el-table-column>
                <el-table-column prop="BrandName" label="品名"></el-table-column>
                <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
                <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
                <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
                <el-table-column prop="PlanEndTime" label="计划完成时间"></el-table-column>
                <el-table-column prop="Describtion" label="描述"></el-table-column>
              </el-table>
              <div class="paginationClass">
                <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
                 :total="total"
                 :current-page="offset"
                 :page-sizes="[5,10,20]"
                 :page-size="tableData.limit"
                 @size-change="handleSizeChange"
                 @current-change="handleCurrentChange">
                </el-pagination>
              </div>
              <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="40%" :append-to-body="true">
                <el-form :model="formField" label-width="110px">
                  <el-form-item label="批次号">
                    <el-input v-model="formField.BatchID"></el-input>
                  </el-form-item>
                  <el-form-item label="计划成品重量">
                    <el-input v-model="formField.PlanQuantity"></el-input>
                  </el-form-item>
                  <el-form-item label="单位">
                    <el-input v-model="formField.Unit"></el-input>
                  </el-form-item>
                  <el-form-item label="计划生产日期">
                    <el-date-picker v-model="formField.PlanDate" type="date" placeholder="选择日期">
                    </el-date-picker>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="dialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="save">保 存</el-button>
                </span>
              </el-dialog>
            </div>
          </el-col>
        </el-col>
        <el-col :span="24" v-if="steps == 1">

        </el-col>
        <el-col :span="24" v-if="steps == 2">

        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "scheduling",
    components:{

    },
    data(){
      return{
        steps:0,
        activeSearch:"PlanStatus",
        productName:"",
        scheduleTableData:[],
        scheduleList:[],
        BrandActive:"",
        BrandCode:"",
        tableData:[],
        limit:5,
        offset:1,
        total:0,
        multipleSelection:[],
        handleType:[
          {type:"primary",label:"添加"},
          {type:"danger",label:"删除"},
        ],
        dialogVisible:false,
        dialogTitle:"",
        formField:{
          BatchID:"",
          PlanQuantity:"",
          Unit:"",
          PlanDate:""
        },
      }
    },
    mounted(){
      this.getScheduleTableData()
    },
    methods:{
      clickStep(index){
        this.steps = index
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
            that.scheduleList = that.scheduleTableData
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
          this.scheduleList = this.scheduleTableData.filter((string) =>{
            return Object.keys(string).some(function(key) {
              return String(string[key]).toLowerCase().indexOf(queryString) > -1
            })
          })
        }else{
          this.scheduleList = this.scheduleTableData
        }
      },
      clickBrandTag(BrandName,BrandCode){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.getTableData(this.BrandActive)
      },
      getTableData(BrandName){
        var that = this
        var params = {
          tableName: "PlanManager",
          field:"BrandName",
          fieldvalue:BrandName,
          limit:this.limit,
          offset:this.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.tableData = res.data.data.rows
            that.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChange(limit){ //每页条数切换
        this.limit = limit
        this.getTableData(this.BrandActive)
      },
      handleCurrentChange(offset) { // 页码切换
        this.offset = offset
        this.getTableData(this.BrandActive)
      },
      handleSelectionChange(row){
        this.multipleSelection = row
      },
      handleForm(label){
        if(label === "添加"){
          if(this.BrandActive){
            this.dialogVisible = true
            this.dialogTitle = label
            this.formField = {
              BatchID:"",
              PlanQuantity:"",
              Unit:"",
              PlanDate:""
            }
          }else{
            this.$message({
              type: 'info',
              message: '请选择品名'
            });
          }
        }else if(label === "删除"){
          var params = {tableName:"PlanManager"}
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
                this.getTableData(this.BrandActive)
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
          var params = {
            BatchID:this.formField.BatchID,
            PlanQuantity:this.formField.PlanQuantity,
            Unit:this.formField.Unit,
            PlanDate:this.formField.PlanDate,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode
          }
          this.axios.post("/api/makePlan",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.dialogVisible = false
              this.getTableData(this.BrandActive)
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
