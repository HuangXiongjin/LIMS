<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">可视化流程管理</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="platformContainer">
            <el-col :span="6" v-for="(item,index) in FlowData" :key="index">
              <el-card shadow="hover" class="marginBottom text-center cursor-pointer">
                <div @click="toG6(item)" :class="{'color-lightgreen':item.ProcessName===selectRow.ProcessName}">
                  <p class="marginBottom-10 text-size-48"><i :class="item.Icon"></i></p>
                  <p class="text-size-16">{{ item.ProcessName }}</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="never" class="text-center cursor-pointer">
                <p class="marginBottom marginTop color-grayblack text-size-48" @click="addFlow"><i class="el-icon-circle-plus-outline"></i></p>
              </el-card>
              <el-dialog title="添加流程" :visible.sync="dialogVisible" width="50%">
                <el-form :model="formParameters" label-width="110px">
                  <el-form-item label="流程名称" >
                    <el-input v-model="formParameters.ProcessName"></el-input>
                  </el-form-item>
                  <el-form-item label="展示图标" >
                    <el-input v-model="formParameters.Icon"></el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="dialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="saveAddFlow">保存</el-button>
                </span>
              </el-dialog>
            </el-col>
          </div>
        </el-col>
        <el-col :span="24">
          <el-form :inline="true">
            <el-form-item>
              <el-button @click="saveFlow">保存流程结构</el-button>
            </el-form-item>
          </el-form>
          <el-row :gutter="20">
            <el-col :span="20">
              <div class="platformContainer">
                <div id="container" style="width: 100%;height: 700px;"></div>
              </div>
            </el-col>
            <el-col :span="4">
              <div class="platformContainer">

              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  import G6 from '@antv/g6';
  export default {
    name: "flowGraph",
    data(){
      return{
        FlowtableName:"TechnologicalProcess",
        FlowData:[],
        dialogVisible:false,
        formParameters:{
          ProcessName:"",
          Icon:""
        },
        selectRow:"",
        selectFlowData:"",
        graph:null,
      }
    },
    mounted() {
      this.getFlow()
    },
    methods:{
      getFlow(){
        var that = this
        var params = {
          tableName: this.FlowtableName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.FlowData = data.rows
          }
        },res =>{
          console.log("请求错误")
        })
      },
      addFlow(){
        this.dialogVisible = true
      },
      saveAddFlow(){
        var params = {
          tableName:this.FlowtableName,
          ProcessName:this.formParameters.ProcessName,
          Icon:this.formParameters.Icon,
        }
        this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data.code === "200"){
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.getFlow()
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
          this.dialogVisible = false
        },res =>{
          console.log("请求错误")
        })
      },
      toG6(label){
        this.selectRow = label
        this.selectFlowData = {}
        this.FlowData.forEach(item =>{
          if(item.ProcessName === label.ProcessName){
            if(item.ProcessStructure === '' || item.ProcessStructure === 'None'){
              this.selectFlowData.id = 'root'
              this.selectFlowData.label = 'root'
            }else{
              this.selectFlowData = JSON.parse(item.ProcessStructure)
            }
          }
        })
        if(this.graph){
          this.graph.destroy()
        }
        this.init()
      },
      saveFlow(){
        var params = {
          tableName:this.FlowtableName,
          ID:this.selectRow.ID,
          ProcessStructure:JSON.stringify(this.graph.save())
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res => {
          console.log(res.data)
          if (res.data.code === "200") {
            this.$message({
              type: 'success',
              message: res.data.message
            });
            this.getFlow()
          } else {
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      init(){
        var that = this
        this.$nextTick(() => {
          const COLLAPSE_ICON = function COLLAPSE_ICON(x, y, r) {
            return [
              ['M', x - r, y - r],
              ['a', r, r, 0, 1, 0, r * 2, 0],
              ['a', r, r, 0, 1, 0, -r * 2, 0],
              ['M', x + 2 - r, y - r],
              ['L', x + r - 2, y - r],
            ];
          };
          const EXPAND_ICON = function EXPAND_ICON(x, y, r) {
            return [
              ['M', x - r, y - r],
              ['a', r, r, 0, 1, 0, r * 2, 0],
              ['a', r, r, 0, 1, 0, -r * 2, 0],
              ['M', x + 2 - r, y - r],
              ['L', x + r - 2, y - r],
              ['M', x, y - 2 * r + 2],
              ['L', x, y - 2],
            ];
          };
          G6.Util.traverseTree(that.selectFlowData, d => {
            d.leftIcon = {
              style: {
                fill: '#e6fffb',
                stroke: '#e6fffb'
              },
              //img: 'https://gw.alipayobjects.com/mdn/rms_f8c6a0/afts/img/A*Q_FQT6nwEC8AAAAAAAAAAABkARQnAQ'
            }
            return true
          })

          G6.registerNode('icon-node', {
            options: {
              size: [60, 20],
              stroke: '#91d5ff',
              fill: '#91d5ff'
            },
            draw(cfg, group) {
              const styles = this.getShapeStyle(cfg)
              const {labelCfg = {}} = cfg

              const keyShape = group.addShape('rect', {
                attrs: {
                  ...styles,
                  x: 0,
                  y: 0
                }
              })

              /**
               * leftIcon 格式如下：
               *  {
               *    style: ShapeStyle;
               *    img: ''
               *  }
               */
              if (cfg.leftIcon) {
                const {style, img} = cfg.leftIcon
                group.addShape('rect', {
                  attrs: {
                    x: 1,
                    y: 1,
                    width: 38,
                    height: styles.height - 2,
                    fill: '#8c8c8c',
                    ...style
                  }
                })

                // group.addShape('image', {
                //   attrs: {
                //     x: 8,
                //     y: 8,
                //     width: 24,
                //     height: 24,
                //     //img: img || 'https://g.alicdn.com/cm-design/arms-trace/1.0.155/styles/armsTrace/images/TAIR.png',
                //   },
                //   name: 'image-shape',
                // });
              }

              // 如果不需要动态增加或删除元素，则不需要 add 这两个 marker
              group.addShape('marker', {
                attrs: {
                  x: 40,
                  y: 52,
                  r: 6,
                  stroke: '#73d13d',
                  cursor: 'pointer',
                  symbol: EXPAND_ICON
                },
                name: 'add-item'
              })

              group.addShape('marker', {
                attrs: {
                  x: 80,
                  y: 52,
                  r: 6,
                  stroke: '#ff4d4f',
                  cursor: 'pointer',
                  symbol: COLLAPSE_ICON
                },
                name: 'remove-item'
              })

              if (cfg.label) {
                group.addShape('text', {
                  attrs: {
                    ...labelCfg.style,
                    text: cfg.label,
                    x: 50,
                    y: 25,
                  }
                })
              }

              return keyShape
            }
          }, 'rect')

          G6.registerEdge('flow-line', {
            draw(cfg, group) {
              const startPoint = cfg.startPoint;
              const endPoint = cfg.endPoint;

              const {style} = cfg
              const shape = group.addShape('path', {
                attrs: {
                  stroke: style.stroke,
                  endArrow: style.endArrow,
                  path: [
                    ['M', startPoint.x, startPoint.y],
                    ['L', startPoint.x, (startPoint.y + endPoint.y) / 2],
                    ['L', endPoint.x, (startPoint.y + endPoint.y) / 2,],
                    ['L', endPoint.x, endPoint.y],
                  ],
                },
              });

              return shape;
            }
          });

          const defaultStateStyles = {
            hover: {
              stroke: '#1890ff',
              lineWidth: 2
            }
          }

          const defaultNodeStyle = {
            fill: '#91d5ff',
            stroke: '#40a9ff',
            radius: 5
          }

          const defaultEdgeStyle = {
            stroke: '#91d5ff',
            endArrow: {
              path: 'M 0,0 L 12, 6 L 9,0 L 12, -6 Z',
              fill: '#91d5ff',
              d: -20
            }
          }

          const defaultLayout = {
            type: 'compactBox',
            direction: 'TB',
            getId: function getId(d) {
              return d.id;
            },
            getHeight: function getHeight() {
              return 16;
            },
            getWidth: function getWidth() {
              return 16;
            },
            getVGap: function getVGap() {
              return 40;
            },
            getHGap: function getHGap() {
              return 70;
            },
          }

          const defaultLabelCfg = {
            style: {
              fill: '#000',
              fontSize: 12
            }
          }

          const width = document.getElementById('container').scrollWidth;
          const height = document.getElementById('container').scrollHeight || 500;

          const minimap = new G6.Minimap({
            size: [150, 100]
          })
          that.graph = new G6.TreeGraph({
            container: 'container',
            width,
            height,
            linkCenter: true,
            plugins: [minimap],
            modes: {
              default: [
                'drag-canvas',
                'zoom-canvas',
              ],
            },
            defaultNode: {
              type: 'icon-node',
              size: [120, 40],
              style: defaultNodeStyle,
              labelCfg: defaultLabelCfg
            },
            defaultEdge: {
              type: 'flow-line',
              style: defaultEdgeStyle,
            },
            nodeStateStyles: defaultStateStyles,
            edgeStateStyles: defaultStateStyles,
            layout: defaultLayout
          });

          that.graph.read(that.selectFlowData);
          that.graph.fitView();

          that.graph.on('node:mouseenter', evt => {
            const {item} = evt
            that.graph.setItemState(item, 'hover', true)
          })

          that.graph.on('node:mouseleave', evt => {
            const {item} = evt
            that.graph.setItemState(item, 'hover', false)
          })

          that.graph.on('node:click', evt => {
            const {item, target} = evt
            const targetType = target.get('type')
            const name = target.get('name')

            // 增加元素
            if (targetType === 'marker') {
              const model = item.getModel()
              if (name === 'add-item') {
                if (!model.children) {
                  model.children = []
                }
                const id = `n-${Math.random()}`;
                model.children.push({
                  id,
                  label: id.substr(0, 8),
                  leftIcon: {
                    style: {
                      fill: '#e6fffb',
                      stroke: '#e6fffb'
                    },
                    img: 'https://gw.alipayobjects.com/mdn/rms_f8c6a0/afts/img/A*Q_FQT6nwEC8AAAAAAAAAAABkARQnAQ'
                  }
                })
                that.graph.updateChild(model, model.id)
              } else if (name === 'remove-item') {
                that.graph.removeChild(model.id)
              }
            }
          })
        })
      }
    }
  }
</script>

<style scoped>

</style>
