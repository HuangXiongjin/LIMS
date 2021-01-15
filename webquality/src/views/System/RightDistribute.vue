<template>
    <el-row :gutter='20'>
        <el-col :span='24'>
            <el-col :span='24' class="container">分配权限列表</el-col>
            <el-col :span='24' class="mgt24 container" :style="conheight" style="overflow:auto;">
                <div class="mgb24">
                    <el-button type="primary" size='small' @click="New('添加')">添加</el-button>
                    <el-button type="success" size='small' @click="New('编辑')">编辑</el-button>
                    <el-button type="warning" size='small' @click="deleteRole">删除</el-button>
                </div>
                <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @selection-change="handleSelectionChange">
                    >
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                </el-table>
                <div class="paginationClass">
                    <el-pagination background  layout="total, prev, pager, next, jumper"
                    :total="batchTableData.total"
                    :current-page="batchTableData.offset"
                    :page-size="batchTableData.limit"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange">
                </el-pagination>
                </div>
            </el-col>
            <el-dialog :title="txt" :visible.sync="dialogTableVisible">
                <el-form label-position="right" label-width="80px" :model="formLabelAlign">
                    <el-form-item label="人物">
                        <el-input v-model="formLabelAlign.man"></el-input>
                    </el-form-item>
                    <el-form-item label="登录名称">
                        <el-input v-model="formLabelAlign.name"></el-input>
                    </el-form-item>
                    <el-form-item label="登录密码">
                        <el-input v-model="formLabelAlign.password"></el-input>
                    </el-form-item>
                    <el-form-item label="对应权限" class="rightDis">
                       <el-select v-model="formLabelAlign.rights" multiple placeholder="请选择">
                            <el-option
                            v-for="item in allrights"
                            :key="item.value"
                            :label="item.label"
                            :value="item.label">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogTableVisible = false">取 消</el-button>
                    <el-button type="primary" @click="Optform">确 定</el-button>
                </div>
            </el-dialog>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
            allrights:[{
                value:'1',
                label:'请验审核'
            },{
                value:'2',
                label:'领样'
            },{
                value:'3',
                label:'样本接收'
            },{
                value:'4',
                label:'样本及记录分发'
            },{
                value:'5',
                label:'质检发送'
            },{
                value:'6',
                label:'质检审核'
            },{
                value:'7',
                label:'报告初审'
            },{
                value:'8',
                label:'报告复审'
            },{
                value:'9',
                label:'销毁审核'
            },{
                value:'10',
                label:'申请销毁'
            },{
                value:'11',
                label:'权限管理'
            }],
            formLabelAlign:{
                name:'',
                password:'',
                man:'',
                rights:[]
            },
            txt:'操作',
            dialogTableVisible:false,
            batchTableData:{ //物料BOM
                data:[],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           Row:{},
           distribute:{
               CheckProjectNO:'',
           },
           conheight:{
                height:''
            },
           searchObj:{
               category:'玉米淀粉',
               DestructionType:'样品销毁',
           },
           options: [{
                value: '选项1',
                label: '物料一'
                }],
           destroys: [{
                value: '样品销毁',
                label: '样品销毁'
                },{
                value: '留样销毁',
                label: '留样销毁'
                }],
            currentRow:[],
            batchtableconfig:[{prop:'Name',label:'人物',width:'100'},{prop:'WorkNumber',label:'登录名称',width:'120'},{prop:'Password',label:'登录密码',width:'120'},{prop:'CreateTime',label:'操作时间',width:'200'},{prop:'Permissions',label:'对应权限'}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.getAllPeople()
       window.addEventListener('resize', this.getHeight);
       this.getHeight()
    },
    beforeRouteEnter(to,from,next){
        if(to.path==='/RightDistribute'){
            if(JSON.parse(sessionStorage.getItem('Rights').replace(/'/g, '"')).includes("权限管理")){
                next()
            }else{
                next('/Nopermission')
            }
        }
    },
    methods: {
        getHeight(){
          this.conheight.height=(window.innerHeight-200)+'px'
       },
        New(txt){
            this.txt=txt
            if(this.txt=='添加'){
                this.dialogTableVisible=true
            }else if(this.txt=='编辑'){
                if(this.currentRow.length==0){
                    this.$message({
                        type:'info',
                        message:'请先勾选要编辑的数据'
                    })
                }else if(this.currentRow.length>=2){
                    this.$message({
                        type:'info',
                        message:'只能编辑一条数据'
                    })
                }else{
                    this.dialogTableVisible=true
                    this.formLabelAlign.name=this.currentRow[0].WorkNumber
                    this.formLabelAlign.password=this.currentRow[0].Password
                    this.formLabelAlign.man=this.currentRow[0].Name
                    this.formLabelAlign.rights=JSON.parse(this.currentRow[0].Permissions.replace(/'/g, '"'))
                }
            }
        },
        handleSelectionChange(row){
            this.currentRow=row
        },
        Optform(){
            if(this.txt=='添加'){
                this.addRole()
            }else if(this.txt=='编辑'){
                this.editRole()
            }
        },
        addRole(){ //添加较色
            var params={
                TableName:'User',
                Values:JSON.stringify({
                    Name:this.formLabelAlign.man,
                    WorkNumber:this.formLabelAlign.name,
                    Password:this.formLabelAlign.password,
                    CreateTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                    Permissions:this.formLabelAlign.rights,
                    OrganizationName:"shiyanshi"
            })
            }
            this.axios.post('/lims/CRUD',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                    this.dialogTableVisible=false
                    this.getAllPeople()
                }else{
                    this.$message({
                        type:'info',
                        message:'添加失败'
                    })
                }
            })
        },
        getAllPeople(){ //获取所有人
            var params={
                TableName:'User',
                Page:this.batchTableData.offset,
                Query:'Accurate',
                PerPage:this.batchTableData.limit,
                QueryColumnName:'OrganizationName',
                QueryColumnValue:'shiyanshi',
            }
            this.axios.get('/lims/CRUD',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
                }
            })
        },
        editRole(){ //编辑角色
           var params={
                TableName:'User',
                ID:this.currentRow[0].ID,
                Values:JSON.stringify({
                    Name:this.formLabelAlign.man,
                    WorkNumber:this.formLabelAlign.name,
                    Password:this.formLabelAlign.password,
                    CreateTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                    Permissions:this.formLabelAlign.rights,
                    OrganizationName:"shiyanshi"
            })
            }
            this.axios.patch('/lims/CRUD',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'编辑成功'
                    })
                    this.dialogTableVisible=false
                    this.getAllPeople()
                }else{
                    this.$message({
                        type:'info',
                        message:'编辑失败'
                    })
                }
            })
        },
        deleteRole(){ //删除角色
            if(this.currentRow.length==0){
                    this.$message({
                        type:'info',
                        message:'请先勾选要删除的数据'
                    })
                }else if(this.currentRow.length>=2){
                    this.$message({
                        type:'info',
                        message:'只能删除一条数据'
                    })
                }else{
                    var params={
                        TableName:'User',
                        ID:this.currentRow[0].ID
                    }
                    this.axios.delete('/lims/CRUD',{params:params}).then((res) => {
                        if(res.data.code=='1000'){
                            this.$message({type:'success',message:'删除成功'})
                            this.getAllPeople()
                        }else{
                            this.$message({type:'info',message:'删除失败'})
                        }
                        })
                    }
        },
         getSelectOption() { //获取下拉列表选项
           this.axios.get('/lims/AllProduct').then((res) => {
               if(res.data.code=='1000'){
                  this.options=res.data.data.map((item) => {
                      return {
                          value:item,
                          label:item
                      }
                  })
               }

           })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.getAllPeople()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.getAllPeople()
        },
    },
}
</script>
<style scoped>

</style>