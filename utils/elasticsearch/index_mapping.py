#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年4月10日
@author: yangxu
'''
cpu_mapping = {
        "settings" : {
                "index" : {
                    "number_of_replicas" : 1 
                        }
                      },
        "mappings" : {
              "cpu" : {
                "properties" : {
                  "host" : {
                    "type" : "string",
                  },
                  "iowait" : {
                    "type" : "float"
                  },
                  "timestamp" : {
                    "type" : "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                  },
                  "usage" : {
                    "type" : "float"
                  }
                }
              }
            }
        }

memory_mapping = {
        "settings" : {
                "index" : {
                    "number_of_replicas" : 1 
                        }
                      },
        "mappings" : {
              "memory" : {
                "properties" : {
                  "host" : {
                    "type" : "string",
                  },
                  "free" : {
                    "type" : "float"
                  },
                  "timestamp" : {
                    "type" : "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                  },
                  "total" : {
                    "type" : "float"
                  }
                }
              }
            }
        }

disk_mapping = {
        "settings" : {
                "index" : {
#                     "number_of_shards" : 3, 
                    "number_of_replicas" : 1 
                        }
                      },
        "mappings" : {
              "disk" : {
                "properties" : {
                  "host" : {
                    "type" : "string",
                  },
                  "partition" : {
                    "type" : "string"
                  },
                  "usage" : {
                    "type" : "float"
                  },
                  "timestamp" : {
                    "type" : "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                  },
                  "free" : {
                    "type" : "float"
                  }
                }
              }
            }
        }


network_mapping = {
        "settings" : {
                "index" : {
#                     "number_of_shards" : 3, 
                    "number_of_replicas" : 1 
                        }
                      },
        "mappings" : {
              "network" : {
                "properties" : {
                  "host" : {
                    "type" : "string",
                  },
                  "device" : {
                    "type" : "string"
                  },
                  "transmit" : {
                    "type" : "long"
                  },
                  "receive" : {
                    "type" : "long"
                  },
                  "drop" : {
                    "type" : "long"
                  },
                  "timestamp" : {
                    "type" : "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                  }
                }
              }
            }
        }