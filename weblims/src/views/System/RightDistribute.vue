<template>
    <el-row :gutter='20'>
        <el-col :span='24'>
            <el-col :span='24' class="container">分配权限列表</el-col>
            <el-col :span='24' class="mgt24 container" style="height:500px;">
                <div class="mgb24">
                    <el-button type="primary" size='small' @click="New('添加')">添加</el-button>
                    <el-button type="success" size='small' @click="New('编辑')">编辑</el-button>
                    <el-button type="warning" size='small'>删除</el-button>
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
                            :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogTableVisible = false">取 消</el-button>
                    <el-button type="primary" @click="dialogTableVisible = false">确 定</el-button>
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
                label:'设备操作'
            },{
                value:'2',
                label:'设备修理'
            },{
                value:'3',
                label:'设备修理'
            },{
                value:'4',
                label:'设备修理'
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
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           Row:{},
           distribute:{
               CheckProjectNO:'',
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
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            currentRow:[],
            batchtableconfig:[{prop:'ProductNumber',label:'人物',width:'100'},{prop:'CheckDepartment',label:'登录名称',width:'120'},{prop:'Name',label:'登录密码',width:'120'},{prop:'CheckDate',label:'操作时间',width:'200'},{prop:'ProductDestruction',label:'对应权限'}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    beforeRouteEnter(to,from,next){
        if(to.path==='/RightDistribute'){
            if(localStorage.getItem('Name')=='xea'){
                next()
            }else{
                next('/Nopermission')
            }
        }
    },
    methods: {
        New(txt){
            this.txt=txt
            this.dialogTableVisible=true
        },
        handleSelectionChange(row){
            this.currentRow=row
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
         SearchTab(){ //查询相关数据
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DestructionType:this.searchObj.DestructionType
            }
            this.axios.get('/lims/DestructionVerify',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        },
    },
}
</script>
<style scoped>

</style>