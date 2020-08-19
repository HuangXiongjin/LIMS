<template>
    <el-row>
        <el-col :span='24' class="productionstep  marginBottom" style="marginTop:10px;">
            <el-steps :active="active" finish-status="success">
                <el-step title="批次号品名录入" icon="el-icon-lock"></el-step>
                <el-step title="批次计划" icon="el-icon-lock"></el-step>
                <el-step title="计划效验结果" icon="el-icon-lock"></el-step>
            </el-steps>
            <!-- <el-button style="margin-top: 12px;" @click="nextStep">下一步</el-button> -->
        </el-col>
        <el-col :span='24' class="cardContainer" v-if='active===0'>
            <div class="text-size-18 marginBottom">计划实际信息</div>
            <el-form :model="formInline" class="demo-form-inline">
                <el-form-item>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">品名</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择品名">
                            <el-option label="区域一" value="shanghai"></el-option>
                            <el-option label="区域二" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">计划重量</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">生产线</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">单位</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择品名">
                            <el-option label="区域一" value="shanghai"></el-option>
                            <el-option label="区域二" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
            </el-form>
        </el-col>
        <el-col>
            <div class="platformContainer" v-if='active===0'>
                <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
            </div>
        </el-col>
        <el-col>
            <div class="platformContainer" v-if='active===1'>
                <div class="marginBottom text-size-18">生成计划信息</div>
                <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
            </div>
        </el-col>
        <el-col v-if="active===2">
            <div class="platformContainer" style="textAlign:center;height:200px;fontSize:20px;lineHeight:200px;">
              计划检验结果：新增计划成功
            </div>
        </el-col>
        <el-col style="textAlign:right;">
            <el-button type="primary" @click="nextStep" >下一步</el-button>
        </el-col>
    </el-row>
</template>
<script>
 import tableView from '@/components/CommonTable'
export default {
    components:{tableView},
    data() {
        return {
            active:0,
            formInline: {
                user: '',
                region: ''
            },
           PermissionTableData:{
            tableName:"ZYTask",
            column:[
                {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
                {prop:"EquipmentID",label:"设备ID",type:"input",value:""},
                {prop:"PlanDate",label:"计划日期",type:"input",value:""},
                {prop:"TaskID",label:"制药任务单号",type:"input",value:""},
                {prop:"BatchID",label:"批次号",type:"input",value:""},
            ],
            data:[],
            limit:5,
            offset:1,
            total:0,
            tableSelection:true, //是否在第一列添加复选框
            searchProp:"",
            searchVal:"",
            multipleSelection: [],
        }
        }
    },
    created(){
      this.getPermissionTable()
    },
    methods:{
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionTableData.tableName,
          limit:this.PermissionTableData.limit,
          offset:this.PermissionTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PermissionTableData.data = data.rows
            that.PermissionTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      nextStep(){
          this.active++
          if(this.active===3){
              this.active=0
          }
      }
    }
}
</script>
<style scoped>
  .productionstep .el-steps--simple{
      background-color:#ddd;
  }
</style>