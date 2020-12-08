<template>
   <el-row :gutter="20">
        <el-col :span='5'>
            <el-col class="container" style="height:600px;overflow:auto;">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                <el-tree
                    :data="treeDom"
                    node-key="id"
                    default-expand-all
                    :expand-on-click-node="false"
                    :props="defaultProps"
                    @node-click='showTabInfo'>
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                    <span>{{ node.label }}</span>
                        <span class="operations">
                            <i v-if="data.hasOwnProperty('children')" @click="() => append(node,data)" class="el-icon-plus greenadd fontsz10"></i><!--增加分组-->
                            <i v-if="!data.hasOwnProperty('children')" @click="() => deletes(node,data)" class="el-icon-delete redde fontsz10"></i><!--删除分组-->
                            <i v-if="!data.hasOwnProperty('children')" @click="() => rename(node,data)" class="el-icon-edit bledit fontsz10"></i><!--重命名分组-->
                        </span>
                    </span>
               </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='19' class="container" style="height:600px;position:relative;">
            <el-col :span='24' class="mgt24">
                <div class="fontWet titl" style="height:40px;lineHeight:30px;borderBottom:1px solid #ccc;">{{currentgoods}}检验项</div>
                <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handleEdit(scope.row)" type="text" size="small" class="bledit">修改</el-button>
                            <el-button @click.native.prevent="handleDelete(scope.$index, batchTableData.data)" type="text" size="small" class="redde">删除</el-button>
                        </template>
                    </el-table-column>
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
            <el-col :span='24' style="textAlign:right;position:absolute;bottom:10px;right:20px;">
                <el-button type="danger" size='mini'>删除</el-button>
                <el-button type="success" size='mini' @click="newMaterial">新增</el-button>
            </el-col>
        </el-col>
        <el-dialog
            title="添加新的节点"
            width="25%"
            class="add-event-dialog"
            :visible.sync="addEventdialogVisible"
            size="tiny">
            <el-form ref="addEventForm" :model="addEventForm">
                <el-form-item label="节点名称" prop="categoryName" >
                <el-input v-model="addEventForm.categoryName"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer" >
                <el-button @click="addEventdialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="editconfirm">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog
            title="添加新的物料类信息"
            width="30%"
            class="add-event-dialog"
            :visible.sync="materialdialogVisible"
            size="tiny">
            <el-form ref="materialForm" :model="MaterialForm" label-width="80px">
                <el-form-item label="产品品名">
                    <el-input v-model="MaterialForm.Product"></el-input>
                </el-form-item>
                <el-form-item label="品名编码">
                    <el-input v-model="MaterialForm.Code"></el-input>
                </el-form-item>
                <el-form-item label="产品类型">
                    <el-input v-model="MaterialForm.Type"></el-input>
                </el-form-item>
                <el-form-item label="产品来源">
                    <el-input v-model="MaterialForm.Source"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                    <el-input v-model="MaterialForm.Uint"></el-input>
                </el-form-item>
                <el-form-item label="录入时间">
                    <el-input v-model="MaterialForm.IntoTime"></el-input>
                </el-form-item>
                <el-form-item label="录入人">
                    <el-input v-model="MaterialForm.IntoUser"></el-input>
                </el-form-item>
                <el-form-item label="修改时间">
                    <el-input v-model="MaterialForm.AlterTime"></el-input>
                </el-form-item>
                <el-form-item label="修改人">
                    <el-input v-model="MaterialForm.AlterUser"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer" >
                <el-button @click="materialdialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="PostMaterialInfo">确 定</el-button>
            </span>
        </el-dialog>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           addEventdialogVisible: false,
           addEventForm:{
            categoryName: '',
            },
           MaterialForm:{ //新增输入框绑定
            Product: '',
            Code:'',
            Type:'',
            Source:'',
            Uint:'',
            IntoTime:'',
            IntoUser:'',
            AlterTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
            AlterUser:localStorage.getItem('Name'),
            },
           materialdialogVisible:false, //新增物料信息卡片
           currentNodeData:{},//rename之后的保存
           currentParent:'',
           currentgoods:'样本',//当前点击的物类
           batchTableData:{ //物料BOM
                tableName:"PlanManager",
                data:[
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三',StandwardDocument:'点击查看'},
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三'},
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三'},
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三'},
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三'},
                    {Product:'巴戟胶囊',Code:'BJJN',Uint:'kg',IntoTime:'2020-12-01 15:54:22',IntoUser:'lig',AlterTime:'2020-12-01 15:54:22',AlterUser:'张三'},
                    ],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Product',label:"名称"},{prop:'Code',label:'物料编码'},{prop:'Uint',label:'单位',width:'60'},{prop:'IntoTime',label:'录入时间',width:'160'},{prop:'IntoUser',label:'录入人'},{prop:'AlterTime',label:'修改时间',width:160},{prop:'AlterUser',label:'修改人'},{prop:'StandwardDocument',label:'项目标准文档'}],//批次列表
            treeDom: [],//渲染的树
            defaultProps: {
                children: 'children',
                label: 'label'
            }
        }
    },
    created(){
        this.getTreeDom()
    },
    methods: {
        showTabInfo(obj,data,node){
            this.currentgoods=obj.label
           //查询对应名字的数据
        },
        getTreeDom(){ //初始化获取树结构
            this.axios.get('/lims/ClassifyTree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data[0].children
                }
            })
        },
        handleEdit(row){ //表格编辑按钮
            console.log(row)
        },
        handleDelete(index,row){ //表格删除按钮
            console.log(index)
            console.log(row)
        },
        PostMaterialInfo(){ //发送录入的详细信息
            var params={
                Product:this.MaterialForm.Product,
                Code:this.MaterialForm.Code,
                Type:this.MaterialForm.Type,
                Source:this.MaterialForm.Source,
                Uint:this.MaterialForm.Uint,
                IntoTime:this.MaterialForm.IntoTime,
                IntoUser:this.MaterialForm.IntoUser,
                AlterTime:this.MaterialForm.AlterTime,
                AlterUser:this.MaterialForm.AlterUser,
            }
            this.batchTableData.data.push(params)
            this.axios.post('https://yapi.baidu.com/mock/10425/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code==200){
                     this.$message({
                        type: 'success',
                        message: '添加成功'
                        });
                }else{
                   this.$message({
                        type: 'success',
                        message: '添加失败，请重试'
                        }); 
                }
                this.materialdialogVisible=false
            })
        },
        newMaterial(){ //命名弹出框
            this.materialdialogVisible=true
        },
        append(node,data) { //添加节点
            const newChild = { id:new Date().getTime(), label: '新增节点'};
            if (!data.children) {
            this.$set(data, 'children', []);
            }
            data.children.push(newChild);
            this.currentParent=data.label
            var params={
                    ParentName:this.currentParent,
                    ChildrenName:'新增节点'
                }
                this.axios.post('https://yapi.baidu.com/mock/10425/ClassifyTree',this.qs.stringify(params)).then((res) => {
                    if(res.data.code=='1000'){
                        this.$message({
                            type:'success',
                            message:'添加节点成功'
                        })
                    }
                })
        },
        deletes(node,data){ //删除节点
            const parent = node.parent;
            const children = parent.data.children || parent.data;
            const index = children.findIndex(d => d.id === data.id);
            this.$confirm('确定要删除该节点吗？', '温馨提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$message({
                type: 'success',
                message: '已删除'
                });
                children.splice(index, 1);

            }).catch(() => {
                this.$message({
                type: 'info',
                message: '已取消删除'
                });
            });
        },
        rename(node,data){ //节点重命名
            this.currentParent=node.parent.data.label
            this.addEventdialogVisible=true
            this.currentNodeData=data
        },
        editconfirm(){ //节点命名修改确认
            if(this.addEventForm.categoryName!=''){
                this.currentNodeData.label=this.addEventForm.categoryName
                this.addEventdialogVisible=false
                var params={
                    ParentName:this.currentParent,
                    ChildrenName:this.addEventForm.categoryName
                }
                this.axios.post('https://yapi.baidu.com/mock/10425/ClassifyTree',this.qs.stringify(params)).then((res) => {
                    console.log(res)
                })
            }else{
                this.$message({
                    type:'error',
                    message:'节点名称不能为空'
                })
            }
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
        },
    },
}
</script>
<style scoped>
    .operations{
        margin-left: 30px;
        position: absolute;
        right: 4px;
    }
    .el-tree-node__content{
        position: relative;
    }
</style>