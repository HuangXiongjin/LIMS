<template>
    <el-row>
        <el-col :span='24' class="productionstep marginBottom">
            <el-steps :active="active" finish-status="success">
                <el-step title="步骤 1" icon="el-icon-edit"></el-step>
                <el-step title="步骤 2" icon="el-icon-upload"></el-step>
                <el-step title="步骤 3" icon="el-icon-picture"></el-step>
            </el-steps>
            <!-- <el-button style="margin-top: 12px;" @click="nextStep">下一步</el-button> -->
        </el-col>
        <el-col :span='24' class="cardContainer">
            <div class="text-size-18 marginBottom">计划实际信息</div>
            <el-form :model="formInline" class="demo-form-inline">
                <el-form-item>
                    <el-col :span='2' style="textAlign:center;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:center;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:center;">品名</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择品名">
                            <el-option label="区域一" value="shanghai"></el-option>
                            <el-option label="区域二" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-col :span='2' style="textAlign:center;">计划重量</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:center;">生产线</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:center;">单位</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择品名">
                            <el-option label="区域一" value="shanghai"></el-option>
                            <el-option label="区域二" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>
</template>
<script>
export default {
    data() {
        return {
            active:0,
            formInline: {
                user: '',
                region: ''
            },
            PermissionTableData:{
                tableName:"ProcessUnit",
                column:[
                    {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
                    {prop:"PUCode",label:"工艺段编码",type:"input",value:""},
                    {prop:"PUName",label:"工艺段名称",type:"input",value:""},
                    {prop:"PRCode",label:"产品定义编码",type:"input",value:""},
                    {prop:"PLineID",label:"生产线ID",type:"input",value:""},
                    {prop:"Desc",label:"描述",type:"input",value:"",searchProp:false,canSubmit:false},
                    {prop:"PURateCapacity",label:"工艺段额定生产能力",type:"input",value:"",searchProp:false,canSubmit:false},
                    {prop:"PUPLanCapacity",label:"工艺段计划生产能力",type:"input",value:""},
                    {prop:"Seq",label:"工艺段顺序号",type:"input",value:""},
                    {prop:"CapacityUnit",label:"能力单位",type:"input",value:""},
                    {prop:"PlaceTime",label:"静置时间",type:"input",value:""},
                    {prop:"TimeUnit",label:"时间单位",type:"input",value:""},
                    {prop:"BatchRunTime",label:"批次运行时间",type:"input",value:""},
                ],
                data:[],
                limit:5,
                offset:1,
                total:0,
                tableSelection:true, //是否在第一列添加复选框
                searchProp:"",
                searchVal:"",
                multipleSelection: [],
                dialogVisible: false,
                dialogTitle:'',
                handleType:[
                    {type:"primary",label:"添加"},
                    {type:"warning",label:"修改"},
                    {type:"danger",label:"删除"},
                ],
                },
        }
    },
    methods: {
        nextStep(){
            this.active++
            if(this.active==3){
                this.active=0
            }
        }
    },
}
</script>
<style scoped>
  .productionstep .el-steps--simple{
      background-color:#ddd;
  }
</style>