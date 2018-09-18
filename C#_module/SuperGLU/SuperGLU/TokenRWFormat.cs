﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace SuperGLU
{
    public class TokenRWFormat
    {
        protected static List<Type> VALID_KEY_TYPES = new List<Type>();
        protected static List<Type> VALID_SEQUENCE_TYPES = new List<Type>();
        protected static List<Type> VALID_ATOMIC_VALUE_TYPES = new List<Type>();
        protected static List<Type> VALID_MAPPING_TYPES = new List<Type>();

        protected static List<Type> VALID_VALUE_TYPES = new List<Type>();
         

        static TokenRWFormat()
        {
            VALID_KEY_TYPES.Add(typeof(String));

            VALID_ATOMIC_VALUE_TYPES.Add(typeof(bool));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(int));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(float));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(String));

            VALID_SEQUENCE_TYPES.Add(typeof(List<>));

            VALID_MAPPING_TYPES.Add(typeof(Dictionary<,>));
        }


        public static StorageToken parse(String input)
        {
            throw new Exception("Method not implmented");
        }


        public static Object serialize(StorageToken data)
        {
            throw new Exception("Method Not Implmented");
        }


        protected static bool isNullOrPrimitive(object input)
        {
            if (input == null)
                return true;

            Type inputClass = input.GetType();

            if (TokenRWFormat.VALID_ATOMIC_VALUE_TYPES.Contains(inputClass))
                return true;

            return false;
        }
     
    }


    public class JSONStandardRWFormat : TokenRWFormat
    {
        private static Dictionary<String, Type> NAME_MAPPING = new Dictionary<string, Type>();
        private static Dictionary<Type, String> TYPE_MAPPING = new Dictionary<Type, string>();

        static JSONStandardRWFormat()
        {
            NAME_MAPPING.Add("bool", typeof(bool));
            NAME_MAPPING.Add("unicode", typeof(String));
            NAME_MAPPING.Add("float", typeof(float));
            NAME_MAPPING.Add("int", typeof(int));
            NAME_MAPPING.Add("tuple", typeof(List<>));
            NAME_MAPPING.Add("long", typeof(long));

            TYPE_MAPPING.Add(typeof(bool), "bool");
            TYPE_MAPPING.Add(typeof(String), "unicode");
            TYPE_MAPPING.Add(typeof(float), "float");
            TYPE_MAPPING.Add(typeof(double), "float");
            TYPE_MAPPING.Add(typeof(short), "int");
            TYPE_MAPPING.Add(typeof(int), "int");
            TYPE_MAPPING.Add(typeof(long), "long");
        }

        public static StorageToken parse(String input)
        {
            return null;
        }

        public static String serialize(StorageToken data)
        {
            return null;
        }


        private static Object makeSerializable(Object data)
        {
            if (data == null)
                return data;

            Type clazz = data.GetType();

            if (VALID_ATOMIC_VALUE_TYPES.Contains(clazz))
                return data;
            //if (VALID_SEQUENCE_TYPES.Contains(clazz)) 

            return null;
        }

    }

}