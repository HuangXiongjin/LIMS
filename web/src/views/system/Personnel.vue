<template>
  <el-row>
    <el-col :span="24">
      <el-col :span="24">
        <div class="page-title">
          <span style="margin-left: 10px;" class="text-size-normol">人员管理</span>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="platformContainer">
          <tableView class="" :tableData="TableData" @getTableData="getTableData" @privileges="privileges" @teamGroup="teamGroup"></tableView>
        </div>
        <el-dialog :title="selectPersonnelName" :visible.sync="dialogVisible" width="50%" :append-to-body="true">
          <el-transfer :titles="['未拥有角色', '已分配角色']" :button-texts="['收回', '分配']" v-model="transferValue" :data="transferData"></el-transfer>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="savePrivileges">保存</el-button>
          </span>
        </el-dialog>
        <el-dialog :title="selectPersonnelName" :visible.sync="teamGroupDialogVisible" width="50%">
          <el-transfer :titles="['未拥有班组', '已分配班组']" :button-texts="['收回', '分配']" v-model="transferTeamGroupValue" :data="transferTeamGroupData"></el-transfer>
          <span slot="footer" class="dialog-footer">
            <el-button @click="teamGroupDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="saveTeamGroup">保存</el-button>
          </span>
        </el-dialog>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  import tableView from '@/components/CommonTable'
  export default {
    name: "Personnel",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"User",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"Name",label:"用户名",type:"input",value:""},
            {prop:"WorkNumber",label:"工号",type:"input",value:""},
            {prop:"Password",label:"密码",type:"input",value:"",showField:false,searchProp:false},
            {prop:"Creater",label:"创建人",type:"input",value:"",searchProp:false,canSubmit:false},
            {prop:"LastLoginTime",label:"最近登录时间",type:"input",value:"",searchProp:false,canSubmit:false},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          tableSelection:true, //是否在第一列添加复选框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加",hasPermissions:['管理人员']},
            {type:"warning",label:"修改",hasPermissions:['管理人员']},
            {type:"danger",label:"删除",hasPermissions:['管理人员']},
            {type:"primary",label:"分配角色",clickEvent:"privileges",hasPermissions:['管理人员']},
            {type:"primary",label:"分配班组",clickEvent:"teamGroup",hasPermissions:['管理人员']},
          ],
        },
        selectPersonnelName:"",
        dialogVisible:false,
        transferValue:[],
        transferData:[],
        teamGroupDialogVisible:false,
        transferTeamGroupValue:[],
        transferTeamGroupData:[],
      }
    },
    created(){

    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        var that = this
        var params = {
          tableName: this.TableData.tableName,
          limit:this.TableData.limit,
          offset:this.TableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.TableData.data = data.rows
            that.TableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        })
      },
      privileges(){
        if(this.TableData.multipleSelection.length === 1){
          this.dialogVisible = true
          this.selectPersonnelName = '为 '+this.TableData.multipleSelection[0].Name+' 分配角色'
          this.transferData = []
          this.transferValue = []
          var that = this
          var params = {
            UserID:this.TableData.multipleSelection[0].ID
          }
          this.axios.get("/api/role_management/selectrolebyuser",{
            params: params
          }).then(res =>{
            res.data.notHaveRows.forEach(item =>{
              that.transferData.push({
                key:item.ID,
                label:item.RoleName
              })
            })
            res.data.existingRows.forEach(item =>{
              that.transferValue.push(item.ID)
            })
          },res =>{
            console.log("获取角色时请求错误")
          })
        }else{
          this.$message({
            type: 'info',
            message: '请选择一位人员进行分配'
          });
        }
      },
      savePrivileges(){
        var selectPermissionArr = []
        this.transferValue.forEach(item =>{
          selectPermissionArr.push(item)
        })
        var params = {
          UserID: this.TableData.multipleSelection[0].ID,
          RoleIDs:JSON.stringify(selectPermissionArr)
        }
        this.axios.post("/api/role_management/saveroleuser",this.qs.stringify(params)).then(res =>{
          if(res.data === "OK"){
            this.$message({
              type: 'success',
              message: '分配成功'
            });
            this.dialogVisible = false
          }
        },res =>{
          console.log("保存角色时请求错误")
        })
      },
      teamGroup(){
        if(this.TableData.multipleSelection.length === 1){
          this.teamGroupDialogVisible = true
          this.selectPersonnelName = '为 '+this.TableData.multipleSelection[0].Name+' 分配班组'
          this.transferTeamGroupData = []
          this.transferTeamGroupValue = []
          var that = this
          var params = {
            userID:this.TableData.multipleSelection[0].ID
          }
          this.axios.get("/api/selectUserShiftsGroup",{
            params: params
          }).then(res =>{
            res.data.notHaveRows.forEach(item =>{
              that.transferTeamGroupData.push({
                key:item.ID,
                label:item.ShiftsGroupName
              })
            })
            res.data.existingRows.forEach(item =>{
              that.transferTeamGroupValue.push(item.ID)
            })
          },res =>{
            console.log("获取班组时请求错误")
          })
        }else{
          this.$message({
            type: 'info',
            message: '请选择一位人员进行分配'
          });
        }
      },
      saveTeamGroup(){
        var selectPermissionArr = []
        this.transferTeamGroupValue.forEach(item =>{
          selectPermissionArr.push(item)
        })
        var params = {
          userID: this.TableData.multipleSelection[0].ID,
          shiftsgroupIDs:JSON.stringify(selectPermissionArr)
        }
        this.axios.post("/api/saveuserusershiftsgroup",this.qs.stringify(params)).then(res =>{
          if(res.data === "OK"){
            this.$message({
              type: 'success',
              message: '分配成功'
            });
            this.teamGroupDialogVisible = false
          }
        },res =>{
          console.log("保存班组时请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
